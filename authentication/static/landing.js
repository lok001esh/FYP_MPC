// JavaScript code for the landing page

document.addEventListener("DOMContentLoaded", function() {
    // Add event listeners to the buttons
    var aboutLink = document.getElementById("about-link");
    var signupLink = document.getElementById("signup-link");
    var loginLink = document.getElementById("login-link");
    var getStartedBtn = document.getElementById("get-started-btn");
  
    aboutLink.addEventListener("click", handleAboutClick);
    signupLink.addEventListener("click", handleSignupClick);
    loginLink.addEventListener("click", handleLoginClick);
    getStartedBtn.addEventListener("click", handleGetStartedClick);
  });
  
  // Event handler for the "About" button click
  function handleAboutClick(event) {
    event.preventDefault();
    // Add your logic for handling the "About" button click
  }
  
  // Event handler for the "Sign Up" button click
  function handleSignupClick(event) {
    event.preventDefault();
    // Add your logic for handling the "Sign Up" button click
  }
  
  // Event handler for the "Login" button click
  function handleLoginClick(event) {
    event.preventDefault();
    // Add your logic for handling the "Login" button click
  }
  
  // Event handler for the "Get Started" button click
  function handleGetStartedClick(event) {
    event.preventDefault();
    // Add your logic for handling the "Get Started" button click
  }
  
// DOMContentLoaded event listener
document.addEventListener('DOMContentLoaded', function() {
    // Get the genre list element
    var genreList = document.querySelector('.genre-list');

    // Define an array of genres
    var genres = [
        'POP', 'Hip-Hop', 'Classical', 'Reggae', 'Jazz', 'Blues', 'Rock', 'Metal', 'Disco'
    ];

    // Function to display genres one after another
    function displayGenres() {
        var index = 0;
        genreList.textContent = genres[index];

        setInterval(function() {
            index = (index + 1) % genres.length;
            genreList.textContent = genres[index];
        }, 1000);
    }

    // Call the displayGenres function
    displayGenres();
});

  