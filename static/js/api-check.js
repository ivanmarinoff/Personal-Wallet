document.addEventListener('DOMContentLoaded', function () {
    const storedApiKey = sessionStorage.getItem('api_key');
    const siteUrl = window.location.origin;  // Capture current site URL


    if (storedApiKey) {
        validateApiKey(storedApiKey, siteUrl);
    } else {
        fetchNewApiKey(siteUrl);
    }
});

function fetchNewApiKey(siteUrl) {
    fetch(`https://api-key-gen.onrender.com/api/get-key/?site_url=${encodeURIComponent(siteUrl)}`)
        .then(response => {
            if (response.status === 403 || response.status === 404) {
                handleInvalidKey();
                return null;
            }
            return response.json();
        })
        .then(data => {
            if (data && data.key) {
                sessionStorage.setItem('api_key', data.key);
                validateApiKey(data.key, siteUrl);
            } else {
                handleInvalidKey();
            }
        })
        .catch(error => {
            console.error('Error fetching API key:', error);
            handleInvalidKey();
        });
}

function validateApiKey(apiKey, siteUrl) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('https://api-key-gen.onrender.com/api/validate-key/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken, },
        body: JSON.stringify({ key: apiKey, site_url: siteUrl }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.detail === "Key validated") {
                displayContent();
            } else {
                handleInvalidKey();
            }
        })
        .catch(error => {
            console.error('Error validating API key:', error);
            handleInvalidKey();
        });
}

// Function to handle invalid or missing API keys
function handleInvalidKey() {
    document.body.innerHTML = "<h1>Error 404: Page Not Found</h1><p>The site could not load because a valid API key is missing.</p>";
}

// Function to display main content without redirecting or reloading
function displayContent() {
    // Directly modify the content of the page without reloading
    // window.location.href = "/landing?api_key_valid=true";
    window.open('#?api_key_valid=true', '_self');
}
