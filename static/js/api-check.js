// document.addEventListener('DOMContentLoaded', function () {
//     // Check for a stored key in session storage
//     const storedApiKey = sessionStorage.getItem('api_key');
//     if (storedApiKey) {
//         // If a key is already stored, validate it
//         validateApiKey(storedApiKey);
//     } else {
//         // Fetch a new API key if none is stored
//         fetchNewApiKey();
//     }
// });
//
// // Function to fetch a new API key from the Django API
// function fetchNewApiKey() {
//     // fetch('https://api-key-gen.onrender.com/api/get-key/')
//     fetch('http://127.0.0.1/api/get-key/')
//         .then(response => {
//             if (response.status === 404) {
//                 handleInvalidKey();
//                 return null;
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data && data.key) {
//                 // Store the key in sessionStorage
//                 sessionStorage.setItem('api_key', data.key);
//                 validateApiKey(data.key);
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
// // Function to validate the API key
// function validateApiKey(apiKey) {
//     const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//     fetch('http://127.0.0.1/api/validate-key/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json', 'X-CSRFToken': csrfToken,
//         },
//         body: JSON.stringify({ key: apiKey }),
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.detail === "Key validated") {
//                 displayContent();  // Load your site content when the key is valid
//             } else {
//                 handleInvalidKey();  // Handle invalid key
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
//  function displayContent() {
// //     // Directly modify the content of the page without reloading
// //     // window.location.href = "/landing?api_key_valid=true";
//    window.open('#?api_key_valid=true', '_self');
//  }

document.addEventListener('DOMContentLoaded', function () {
    const storedApiKey = sessionStorage.getItem('api_key');
    const siteUrlElement = document.querySelector('meta[name="site_url"]');
    const siteUrl = siteUrlElement ? siteUrlElement.getAttribute('content') : window.location.origin;


    if (storedApiKey) {
        validateApiKey(storedApiKey, siteUrl);
    } else {
        fetchNewApiKey(siteUrl);
    }
});

function fetchNewApiKey() {
    fetch(`https://keygenapi-0yc8.onrender.com/api/get-key/`)  // No need to pass `site_url`
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

function validateApiKey(apiKey, siteUrl) {
    // Retrieve the CSRF token from the meta tag in the HTML
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('https://keygenapi-0yc8.onrender.com/api/validate-key/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // Include the CSRF token here
        },
        body: JSON.stringify({ key: apiKey, site_url: siteUrl }),
        credentials: 'include'  // Include credentials for cross-origin requests if necessary
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
    document.body.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: center; height: 100vh; text-align: center; text-transform: uppercase;">
            <div>
                <h1 style="color:red">You do not have access rights to this page!</h1>
                <h2 style="color:red" text-style="bold" text-transform: uppercase;>Please contact the administrator -> <a href="https://ivanmarinoff-resume.onrender.com" target="_blank" rel="noopener noreferrer">
                        Copyright &copy; 2024
                        ivanmarinoff</a></h2>
            </div>
        </div>
    `;
}


// Function to display main content without redirecting or reloading
function displayContent() {
    window.open('#', '_self');
}