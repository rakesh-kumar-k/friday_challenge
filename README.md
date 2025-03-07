# Movie Parody Generator

A web application that generates humorous parodies of movie plots using OpenAI's API.

## Features

- Search for movies by title
- Fetch movie details from Wikipedia (plot, year, genre, poster)
- Generate a parody of the movie plot using OpenAI's API
- Display the results in a clean, modern UI

## Architecture

This application uses a client-server architecture:

- **Frontend**: HTML, CSS, and JavaScript
- **Backend**: Python with FastAPI
- **APIs**: Wikipedia API (via Python) and OpenAI API

## Setup Instructions

### Prerequisites

- Python 3.7+ installed
- Node.js and npm (optional, for serving the frontend)
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Edit the `.env` file in the backend directory
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

4. Start the backend server:
   ```
   python app.py
   ```
   The server will run at http://localhost:8000

### Frontend Setup

The frontend is static HTML, CSS, and JavaScript, so you can simply open the `index.html` file in a web browser. However, for the best experience, you can use a simple HTTP server:

Using Python:
```
python -m http.server
```
Then open http://localhost:8000 in your browser.

Using Node.js:
```
npx serve
```
Then open the URL provided in the terminal.

## Usage

1. Enter a movie title in the search box
2. Click "GENERATE" or press Enter
3. Wait for the application to fetch the movie details and generate a parody
4. View the results, including the movie poster, details, and parody summary

## API Documentation

The backend provides a FastAPI-generated Swagger UI documentation at http://localhost:8000/docs when the server is running.

## Technologies Used

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Fetch API

- **Backend**:
  - Python
  - FastAPI
  - Wikipedia API
  - OpenAI API

## License

See the LICENSE file for details.
