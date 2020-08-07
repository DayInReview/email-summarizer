const { spawn } = require('child_process');
const ipcRenderer = require('electron').ipcRenderer;

function getSummaries (email, password) {
    const summary = spawn('python', ['app.py',
                                    '-e', email,
                                    '-p', password]);

    // log everything to console
    summary.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    summary.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

    summary.on('close', (code) => {
        console.log(`child process exited with code: ${code}`);
    });

    // load to home page
    summary.stdout.on('data', (data) => {
        document.getElementById("summary").innerHTML = data;
    });
}

ipcRenderer.on('loginInfo', (event, arg) => {
    getSummaries(arg.email, arg.password);
});