document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');
    // API endpoint - use environment-specific URL
    const API_URL ='https://movie-parody-generator-backend.onrender.com/api/search';
    
    console.log('Using API URL:', API_URL);
    
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
        console.log('handleSearch called');
        const movieName = movieInput.value.trim();
        console.log('movieName:', movieName);
        
        if (!movieName) {
            showError('Please enter a movie title');
            return;
        }
        console.log('movieName is valid');

        // Reset UI
        hideResults();
        hideError();
        showLoader();
        console.log('Fetching movie data from API');

        try {
            console.log('Sending request to:', API_URL);
            console.log('Request payload:', JSON.stringify({ movie_name: movieName }));
            
            // Call the Python backend API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ movie_name: movieName }),
            });
            console.log('API response status:', response.status);
            console.log('API response headers:', Object.fromEntries([...response.headers]));
            
            if (!response.ok) {
                try {
                    const errorData = await response.json();
                    console.error('Error data:', errorData);
                    throw new Error(errorData.detail || 'Failed to fetch movie data');
                } catch (jsonError) {
                    console.error('Error parsing error response:', jsonError);
                    throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
                }
            }
            
            console.log('API response is ok');
            
            const movieData = await response.json();
            console.log('movieData:', movieData);
            
            if (!movieData || !movieData.plot) {
                throw new Error('Could not find movie plot');
            }
            console.log('movieData has plot');
            
            // Display results
            displayResults(movieData);
        } catch (error) {
            console.error('Error:', error);
            showError(error.message || 'An error occurred. Please try again.');
        } finally {
            hideLoader();
            console.log('handleSearch finished');
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
