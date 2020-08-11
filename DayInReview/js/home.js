const { spawn } = require('child_process');
const ipcRenderer = require('electron').ipcRenderer;

ipcRenderer.on('loginInfo', (event, arg) => {
    getSummaries(arg.email, arg.password);
});

// runs when user logs in
function getSummaries(email, password) {
    const summary = spawn('python', ['app.py', '-e', email, '-p', password]);

    summary.stdout.on('data', (data) => {
        var parsed = data.toString() // grab the email_summaries from the python script
        
        // these lines put the string in correct JSON format, JSON is stupid
        parsed = parsed.replace(/'/g, "\""); // replace all the single quotes with double quotes
        parsed = parsed.replace(/\\n/g, "<br>"); // replace all the \n with \\n
        
        parsed = JSON.parse(parsed); // parse parsed with JSON
        console.log(parsed); // log everything to console
        
        loadHomePage(parsed);
    });
}

// window.onload = function() { // loads content when the page is refreshed

// }

function loadHomePage(parsed) {
    document.getElementById("from").innerHTML = parsed[0]['from'];
    document.getElementById("subject").innerHTML = parsed[0]['subject'];
    document.getElementById("date").innerHTML = parsed[0]['date'];
    document.getElementById("time").innerHTML = parsed[0]['time'];
    document.getElementById("summary").innerHTML = parsed[0]['summary'];
}