import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_parody(plot, title):
    """
    Generate a parody of a movie plot using OpenAI's API.
    
    Args:
        plot (str): The original movie plot
        title (str): The movie title
        
    Returns:
        str: The generated parody
    """
    if not openai.api_key:
        return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    
    try:
        # Create a prompt for the OpenAI API
        prompt = f"""
        Generate an absolutely hilarious parody of the following movie plot. Your parody should:
        - Use ridiculous character names that sound similar to the originals but are comically absurd
        - Exaggerate the most serious plot elements to absurd extremes
        - Insert completely illogical plot twists that make no sense but are very funny
        - Include at least one running gag or catchphrase
        - Reference other movies or pop culture in unexpected ways
        - Point out plot holes or movie clichés in a meta, fourth-wall-breaking way
        - Replace dramatic moments with mundane, everyday concerns (like characters stopping mid-action scene to worry about their taxes)

        The parody should be max 5 sentences long and maintain the core story elements while making them ridiculous. Make it so funny that readers will laugh out loud.
        
        Movie Title: {title}
        
        Original Plot: {plot}
        
        Parody:
        """
        
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # You can change this to a different model if needed
            messages=[
                {"role": "system", "content": "You are a brilliant comedy writer known for creating hilarious movie parodies that make people laugh out loud. You specialize in absurdist humor, clever wordplay, and satirical takes on popular films."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.85,  # Higher values make output more random
            top_p=1.0,
            frequency_penalty=0.5,  # Reduce repetition
            presence_penalty=0.5,  # Encourage diversity
        )
        
        # Extract and return the generated parody
        parody = response.choices[0].message.content.strip()
        return parody
    
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return f"Error generating parody: {str(e)}"

# Alternative implementation using the newer OpenAI client library
# Uncomment this and comment out the above function if using the latest OpenAI Python library
"""
def generate_parody(plot, title):
    if not openai.api_key:
        return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    
    try:
        # Create a prompt for the OpenAI API
        prompt = f'''
        Generate an absolutely hilarious parody of the following movie plot. Your parody should:
        - Use ridiculous character names that sound similar to the originals but are comically absurd
        - Exaggerate the most serious plot elements to absurd extremes
        - Insert completely illogical plot twists that make no sense but are very funny
        - Include at least one running gag or catchphrase
        - Reference other movies or pop culture in unexpected ways
        - Point out plot holes or movie clichés in a meta, fourth-wall-breaking way
        - Replace dramatic moments with mundane, everyday concerns (like characters stopping mid-action scene to worry about their taxes)

        The parody should be 5-10 sentences long and maintain the core story elements while making them ridiculous. Make it so funny that readers will laugh out loud.
        
        Movie Title: {title}
        
        Original Plot: {plot}
        
        Parody:
        '''
        
        # Call the OpenAI API
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a brilliant comedy writer known for creating hilarious movie parodies that make people laugh out loud. You specialize in absurdist humor, clever wordplay, and satirical takes on popular films."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.85,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.5,
        )
        
        # Extract and return the generated parody
        parody = response.choices[0].message.content.strip()
        return parody
    
    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return f"Error generating parody: {str(e)}"
"""
