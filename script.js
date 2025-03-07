document.addEventListener('DOMContentLoaded', () => {
    // API endpoint
    const API_URL = 'http://localhost:8000/api/search';
    
    // DOM Elements
    const movieInput = document.getElementById('movie-input');
    const searchBtn = document.getElementById('search-btn');
    const loader = document.getElementById('loader');
    const errorMessage = document.getElementById('error-message');
    const results = document.getElementById('results');
    const moviePoster = document.getElementById('movie-poster');
    const movieTitle = document.getElementById('movie-title');
    const movieYear = document.getElementById('movie-year');
    const movieGenre = document.getElementById('movie-genre');
    const parodyText = document.getElementById('parody-text');

    // Event Listeners
    searchBtn.addEventListener('click', handleSearch);
    movieInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });

    // Main search handler
    async function handleSearch() {
        const movieName = movieInput.value.trim();
        
        if (!movieName) {
            showError('Please enter a movie title');
            return;
        }

        // Reset UI
        hideResults();
        hideError();
        showLoader();

        try {
            // Call the Python backend API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ movie_name: movieName }),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to fetch movie data');
            }
            
            const movieData = await response.json();
            
            if (!movieData || !movieData.plot) {
                throw new Error('Could not find movie plot');
            }
            
            // Display results
            displayResults(movieData);
        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'An error occurred. Please try again.');
        } finally {
            hideLoader();
        }
    }

    // UI Functions
    function showLoader() {
        loader.classList.add('visible');
    }

    function hideLoader() {
        loader.classList.remove('visible');
    }

    function showError(message) {
        errorMessage.textContent = message || 'An error occurred. Please try again.';
        errorMessage.classList.add('visible');
    }

    function hideError() {
        errorMessage.classList.remove('visible');
    }

    function hideResults() {
        results.classList.remove('visible');
    }

    function displayResults(movieData) {
        // Set movie details
        movieTitle.textContent = movieData.title;
        movieYear.textContent = movieData.year || '';
        movieGenre.textContent = movieData.genres || '';
        moviePoster.src = movieData.imageUrl || 'https://via.placeholder.com/300x450?text=No+Image+Available';
        parodyText.textContent = movieData.parody;
        
        // Show results
        results.classList.add('visible');
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});
