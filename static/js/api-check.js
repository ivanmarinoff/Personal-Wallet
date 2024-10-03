document.addEventListener('DOMContentLoaded', function () {
    // Check for a stored key in session storage
    const storedApiKey = sessionStorage.getItem('api_key');
    if (storedApiKey) {
        // If a key is already stored, validate it
        validateApiKey(storedApiKey);
    } else {
        // Fetch a new API key if none is stored
        fetchNewApiKey();
    }
});

// Function to fetch a new API key from the Django API
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
                // Store the key in sessionStorage
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

// Function to validate the API key
function validateApiKey(apiKey) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('https://api-key-gen.onrender.com/api/validate-key/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ key: apiKey }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.detail === "Key validated") {
                displayContent();  // Load your site content when the key is valid
            } else {
                handleInvalidKey();  // Handle invalid key
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

 function displayContent() {
//     // Directly modify the content of the page without reloading
//     // window.location.href = "/landing?api_key_valid=true";
   window.open('#?api_key_valid=true', '_self');
 }

// document.addEventListener('DOMContentLoaded', function () {
//     const storedApiKey = sessionStorage.getItem('api_key');
//     const siteUrlElement = document.querySelector('meta[name="site_url"]');
//     const siteUrl = siteUrlElement ? siteUrlElement.getAttribute('content') : window.location.origin;
//
//
//     if (storedApiKey) {
//         validateApiKey(storedApiKey, siteUrl);
//     } else {
//         fetchNewApiKey(siteUrl);
//     }
// });
//
// function fetchNewApiKey(siteUrl) {
//     fetch(`https://api-key-gen.onrender.com/api/get-key/?site_url=${encodeURIComponent(siteUrl)}`)
//         .then(response => {
//             if (response.status === 403 || response.status === 404) {
//                 handleInvalidKey();
//                 return null;
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data && data.key) {
//                 sessionStorage.setItem('api_key', data.key);
//                 validateApiKey(data.key, siteUrl);
//             } else {
//                 handleInvalidKey();
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching API key:', error);
//             handleInvalidKey();
//         });
// }
//
// function validateApiKey(apiKey, siteUrl) {
//     const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//     fetch('https://api-key-gen.onrender.com/api/validate-key/', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken, },
//         body: JSON.stringify({ key: apiKey, site_url: siteUrl }),
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.detail === "Key validated") {
//                 displayContent();
//             } else {
//                 handleInvalidKey();
//             }
//         })
//         .catch(error => {
//             console.error('Error validating API key:', error);
//             handleInvalidKey();
//         });
// }
//
// // Function to handle invalid or missing API keys
// function handleInvalidKey() {
//     document.body.innerHTML = "<h1>Error 404: Page Not Found</h1><p>The site could not load because a valid API key is missing.</p>";
// }
//
// // Function to display main content without redirecting or reloading
// function displayContent() {
//     // Directly modify the content of the page without reloading
//     // window.location.href = "/landing?api_key_valid=true";
//     window.open('#?api_key_valid=true', '_self');
// }
