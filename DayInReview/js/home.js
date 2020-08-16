const { spawn } = require('child_process');
const ipcRenderer = require('electron').ipcRenderer;

// loads content when the page is refreshed
window.onload = function() {
    loadHomePage(0);
    addRowHandlers();
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
        
        // invalid login
        if (code == 1) {
            window.location.href = "login.html";
        }

        // no emails in inbox
        if (code == 2) {
            console.log("No emails in inbox");
            // window.location.href = "home.html"
            // document.getElementById("no-emails").style.visibility = "visible";
            // document.getElementById("sidebar-table").style.visibility = "hidden";
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
    });
}

function loadHomePage(current_email) {
    var all_emails = JSON.parse(localStorage.getItem('emails'));
    console.log(all_emails);

    document.getElementById("from").innerHTML = all_emails[current_email]['from'];
    document.getElementById("subject").innerHTML = all_emails[current_email]['subject'];
    document.getElementById("date").innerHTML = all_emails[current_email]['date'];
    document.getElementById("time").innerHTML = all_emails[current_email]['time'];
    document.getElementById("summary").innerHTML = all_emails[current_email]['summary'];
}
