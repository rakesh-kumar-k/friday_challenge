from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import wikipedia
import openai_client
import os
import re
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()

# Define request model
class MovieRequest(BaseModel):
    movie_name: str

# Define response model
class MovieResponse(BaseModel):
    title: str
    plot: str
    year: str
    genres: str
    imageUrl: Optional[str] = None
    parody: str

app = FastAPI(title="Movie Parody Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/api/search", response_model=MovieResponse)
async def search_movie(request: MovieRequest):
    """
    Endpoint to search for a movie, get its details from Wikipedia,
    and generate a parody using Google Gemini.
    """
    movie_name = request.movie_name
    
    if not movie_name:
        raise HTTPException(status_code=400, detail="Movie name is required")
    
    try:
        # Search Wikipedia for the movie
        movie_details = search_wikipedia(movie_name)
        
        if not movie_details:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        # Generate parody using Google Gemini
        if movie_details.get('plot'):
            plot = movie_details['plot']
            title = movie_details['title']

            # Extract key details
            key_details = openai_client.extract_key_details(plot, title)

            # Generate parody
            parody = openai_client.generate_parody(key_details, title)

            # Review parody (currently using default feedback)
            parody = openai_client.review_parody(parody)

            movie_details['parody'] = parody
        else:
            movie_details['parody'] = "Could not generate parody due to missing plot information."
        
        return movie_details
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def search_wikipedia(query):
    """
    Search Wikipedia for a movie and extract its details.
    """
    try:
        # First try with 'film' appended to get more relevant results
        search_results = wikipedia.search(query + ' film', results=5)
        
        # If no results, try just the movie name
        if not search_results:
            search_results = wikipedia.search(query, results=5)
            
        if not search_results:
            return None
        
        # Try to find the most relevant page
        movie_page = None
        for result in search_results:
            try:
                page = wikipedia.page(result, auto_suggest=False)
                # Check if it's likely a film page
                content = page.content.lower()
                if ('film' in content or 'movie' in content or 'directed by' in content or 
                    'starring' in content or 'release date' in content):
                    movie_page = page
                    break
            except:
                continue
        
        # If no obvious film found, try the first result
        if not movie_page and search_results:
            try:
                movie_page = wikipedia.page(search_results[0], auto_suggest=False)
            except:
                pass
        
        if not movie_page:
            return None
        
        # Extract movie details
        title = movie_page.title
        
        # Extract plot
        content = movie_page.content
        plot = extract_plot(content)
        
        # Extract year
        year = extract_year(content, title)
        
        # Extract genres
        genres = extract_genres(content)
        
        # Get image URL
        image_url = None
        if movie_page.images:
            for img in movie_page.images:
                if 'poster' in img.lower() or 'cover' in img.lower():
                    image_url = img
                    break
            
            # If no poster found, use the first image
            if not image_url and movie_page.images:
                image_url = movie_page.images[0]
        
        return {
            'title': title,
            'plot': plot,
            'year': year,
            'genres': genres,
            'imageUrl': image_url
        }
    
    except Exception as e:
        print(f"Wikipedia search error: {str(e)}")
        return None

def extract_plot(content):
    """
    Extract the plot section from Wikipedia content.
    """
    # Try to find the plot section
    plot_section = None
    
    # Common section titles for plot
    plot_headers = ['Plot', 'Plot summary', 'Synopsis', 'Storyline', 'Summary']
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        for header in plot_headers:
            if line.strip() == header:
                # Found a plot section, extract text until the next section
                plot_section = []
                j = i + 1
                while j < len(lines) and not lines[j].strip().endswith(':') and not lines[j].strip() in plot_headers:
                    if lines[j].strip():  # Skip empty lines
                        plot_section.append(lines[j])
                    j += 1
                break
        
        if plot_section:
            break
    
    # If no dedicated plot section found, use the first few paragraphs
    if not plot_section:
        plot_section = []
        paragraph_count = 0
        for line in lines:
            if line.strip() and not line.strip().endswith(':'):
                plot_section.append(line)
                paragraph_count += 1
                if paragraph_count >= 3:  # Use first 3 paragraphs
                    break
    
    return ' '.join(plot_section) if plot_section else "Plot not available."

def extract_year(content, title):
    """
    Extract the release year from Wikipedia content.
    """
    # Try to find year in the title
    import re
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', title)
    if year_match:
        return year_match.group(0)
    
    # Try to find year in the content
    year_match = re.search(r'released in (\d{4})', content)
    if year_match:
        return year_match.group(1)
    
    year_match = re.search(r'release date.*?(\d{4})', content, re.IGNORECASE)
    if year_match:
        return year_match.group(1)
    
    # Look for any 4-digit year in the first few paragraphs
    paragraphs = content.split('\n')[:5]
    for paragraph in paragraphs:
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', paragraph)
        if year_match:
            return year_match.group(0)
    
    return "Unknown Year"

def extract_genres(content):
    """
    Extract genres from Wikipedia content.
    """
    genre_keywords = [
        'action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 
        'documentary', 'drama', 'family', 'fantasy', 'film-noir', 'history', 
        'horror', 'music', 'musical', 'mystery', 'romance', 'sci-fi', 
        'science fiction', 'sport', 'superhero', 'thriller', 'war', 'western'
    ]
    
    found_genres = []
    
    # Look for genre mentions
    for genre in genre_keywords:
        # Check for common patterns like "is a [genre] film"
        patterns = [
            rf'is an? {genre} film',
            rf'is an? {genre} movie',
            rf'{genre} film',
            rf'{genre} movie',
            rf'genre.*?{genre}'
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_genres.append(genre.capitalize())
                break
    
    return ', '.join(found_genres) if found_genres else "Unknown Genre"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
