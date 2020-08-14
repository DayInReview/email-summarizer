const { spawn } = require('child_process');
const ipcRenderer = require('electron').ipcRenderer;
const nunjucks = require('nunjucks');
nunjucks.configure({ autoescape: true });

// loads content when the page is refreshed
window.onload = function() {
    loadHomePage();
}

ipcRenderer.on('loginInfo', (event, arg) => {
    getSummaries(arg.email, arg.password);
});

// runs when user logs in
function getSummaries(email, password) {
    localStorage.clear();
    
    const summary = spawn('python', ['app.py', '-e', email, '-p', password]);

    summary.on('close', (code) => {
        console.log(`child process exited with code: ${code}`);
        if (code == 1) {
            window.location.href = "login.html";
        }
    });

    summary.stdout.on('data', (data) => {
        var parsed = data.toString(); // grab the email_summaries from the python script

        // puts content in correct JSON/HTML format
        parsed = parsed.replace(/</g, "&lt"); // escape all left angle brackets
        parsed = parsed.replace(/>/g, "&gt"); // escape all right angle brackets
        parsed = parsed.replace(/'/g, "\""); // replace all the single quotes with double quotes
        parsed = parsed.replace(/\\n/g, " "); // replace all the newlines with a space
        
        parsed = JSON.parse(parsed); // convert stdout to JSON object
        parsed = JSON.stringify(parsed); // convert JSON object to string

        console.log(parsed); // log summaries to console
        window.location.href = "home.html";
        localStorage.setItem('emails', parsed); // store JSON string in local storage
        loadHomePage();
    });
}

function loadHomePage() {
    var all_emails = JSON.parse(localStorage.getItem('emails'));
    console.log(all_emails);
    console.log(all_emails.length);
    document.getElementById("from").innerHTML = all_emails[0]['from'];
    document.getElementById("subject").innerHTML = all_emails[0]['subject'];
    document.getElementById("date").innerHTML = all_emails[0]['date'];
    document.getElementById("time").innerHTML = all_emails[0]['time'];
    document.getElementById("summary").innerHTML = all_emails[0]['summary'];
}