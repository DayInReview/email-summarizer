const { exec } = require('child_process');
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

    exec(`python app.py -e ${email} -p ${password}`, (error, stdout, stderr) => {
        // puts content in correct JSON/HTML format
        parsed = stdout.replace(/</g, "&lt"); // escape all left angle brackets
        parsed = parsed.replace(/>/g, "&gt"); // escape all right angle brackets
        parsed = parsed.replace(/\\n/g, " "); // replace all the newlines with a space
        console.log(stdout);
        
        parsed = JSON.parse(parsed); // convert stdout to JSON object
        parsed = JSON.stringify(parsed); // convert JSON object to string

        console.log(parsed); // log summaries to console
        window.location.href = "home.html";
        localStorage.setItem('emails', parsed); // store JSON string in local storage
        loadHomePage();
    }).on('exit', (code) => {
        console.log(`child process exited with code: ${code}`);
    });
}

function loadHomePage() {
    var all_emails = Object.values(JSON.parse(localStorage.getItem('emails')));
    console.log(all_emails);
    console.log(all_emails.length);
    document.getElementById("from").innerHTML = all_emails[0]['from'];
    document.getElementById("subject").innerHTML = all_emails[0]['subject'];
    document.getElementById("date").innerHTML = all_emails[0]['date'];
    document.getElementById("time").innerHTML = all_emails[0]['time'];
    document.getElementById("summary").innerHTML = all_emails[0]['summary'];
}