const { exec } = require('child_process');
const ipcRenderer = require('electron').ipcRenderer;

ipcRenderer.on('loginInfo', (event, arg) => {
    getSummaries(arg.email, arg.password);
});

// runs when user logs in
function getSummaries(email, password) {
    localStorage.clear();

    exec(`python app.py -e ${email} -p ${password}`, (error, stdout, stderr) => {
        if (error) {
            // invalid login
            if (error.code == 1) {
                console.log("Invalid login");
                // window.location.href = "login.html";
            }
    
            // no emails in inbox
            if (error.code == 2) {
                console.log("No emails in inbox");
                // window.location.href = "home.html"
                // document.getElementById("no-emails").style.visibility = "visible";
                // document.getElementById("sidebar-table").style.visibility = "hidden";
            }
        }

        // puts content in correct JSON/HTML format
        parsed = stdout.replace(/</g, "&lt"); // escape all left angle brackets
        parsed = parsed.replace(/>/g, "&gt"); // escape all right angle brackets
        parsed = parsed.replace(/\\n/g, " "); // replace all the newlines with a space

        parsed = JSON.parse(parsed); // convert stdout to JSON object
        parsed = JSON.stringify(parsed); // convert JSON object to string

        console.log(parsed); // log summaries to console
        window.location.href = "home.html";
        localStorage.setItem('emails', parsed); // store JSON string in local storage
    });
}