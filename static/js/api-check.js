document.addEventListener('DOMContentLoaded', function () {
    // Check for a stored key in session storage
    const storedApiKey = sessionStorage.getItem('api_key');
    if (storedApiKey) {
        validateApiKey(storedApiKey);
    } else {
        // Fetch a new API key from the Django API and validate it
        fetchNewApiKey();
    }
});

function fetchNewApiKey() {
    fetch('https://api-key-gen.onrender.com/api/get-key/')
        .then(response => {
            if (response.status === 404) {
                handleInvalidKey();
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.key) {
                sessionStorage.setItem('api_key', data.key);
                validateApiKey(data.key);
            } else {
                handleInvalidKey();
            }
        })
        .catch(error => {
            console.error('Error fetching API key:', error);
            handleInvalidKey();
        });
}

function validateApiKey(apiKey) {
    fetch('https://api-key-gen.onrender.com/api/validate-key/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key: apiKey }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.detail === "Key validated") {
                displayContent(); // Load your site content
            } else {
                handleInvalidKey();
            }
        })
        .catch(error => {
            console.error('Error validating API key:', error);
            handleInvalidKey();
        });
}

function handleInvalidKey() {
    // Handle the case when API key is invalid or not found
    document.body.innerHTML = "<h1>Error 404: Page Not Found</h1><p>The site could not load because a valid API key is missing.</p>";
}

function displayContent() {
    // Display your main content here
    document.body.innerHTML = "<h1>Welcome to My Site</h1><p>The API key is valid, and the content is loaded.</p>";
}
