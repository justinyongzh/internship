/*===== LOGIN SHOW and HIDDEN =====*/
// Get a reference to the button element
const button = document.getElementById('login-in');

// Add a click event listener to the button
button.addEventListener('click', function() {
    // event.preventDefault(); // Prevent the default form submission behavior
    // const email = document.getElementById('login_username').value;
    // const password = document.getElementById('login_password').value;
    
    // // Extract the role from the email
    // let role;
    // if (email.endsWith('@student.com')) {
    //   role = 'student';
    //   window.location.href = 'user_page.html';
    // } else if (email.endsWith('@admin.com')) {
    //   role = 'admin';
    //   window.location.href = 'admin.html';
      
    // } else if (email.endsWith('@lecturer.com')) {
    //   role = 'lecturer';
    //   window.location.href = 'lecture.html';

    // } else if (email.endsWith('@company.com')) {
    //   role = 'company';
    //   window.location.href = 'index.html';
    // } else {
    //   // Handle unrecognized email pattern or role
    //   console.error('Unrecognized email pattern or role');
    //   return;
    // }
    // Redirect to another HTML page
       window.location.href = '../../templates/home.html';
    
});
