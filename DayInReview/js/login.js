const ipcRenderer = require('electron').ipcRenderer;

function login () {
    console.log("Submitted successfully");
    let email = document.getElementById('email');
    let password = document.getElementById('password');
    ipcRenderer.send('loginInfo', {email: email.value, password: password.value});
    window.close();
}

function invalidLogin () {
    document.getElementById("invalid-login").style.visibility = "visible";
    window.location.href = "login.html";
}