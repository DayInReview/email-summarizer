const { app, BrowserWindow, Menu } = require('electron')
const ipcMain = require('electron').ipcMain;
const path = require('path')
const isMac = process.platform === 'darwin';
const template = [

    // { role: 'appMenu' }
    ...(isMac ? [{
      label: app.name,
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideothers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    }] : []),
    // { role: 'Dev-Mode' }
    {
        label: 'Debug (Dev-Mode)',
        submenu: [
            { role: 'reload' },
            { role: 'toggledevtools' },
            {
                label: 'GitHub Repository',
                click: async () => {
                  const { shell } = require('electron')
                  await shell.openExternal('https://github.com/ishan0102/day-in-review')
                }
            }
        ]
    },
    // { role: 'fileMenu' }
    {
      label: 'File',
      submenu: [
        isMac ? { role: 'close' } : { role: 'quit' }
      ]
    },
    // { role: 'editMenu' }
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        ...(isMac ? [
          { role: 'pasteAndMatchStyle' },
          { role: 'delete' },
          { role: 'selectAll' },
          { type: 'separator' },
          {
            label: 'Speech',
            submenu: [
              { role: 'startspeaking' },
              { role: 'stopspeaking' }
            ]
          }
        ] : [
          { role: 'delete' },
          { type: 'separator' },
          { role: 'selectAll' }
        ])
      ]
    },
    // { role: 'viewMenu' }
    {
      label: 'View',
      submenu: [
        { role: 'toggledevtools' },
        { type: 'separator' },
        { role: 'resetzoom' },
        { role: 'zoomin' },
        { role: 'zoomout' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    // { role: 'windowMenu' }
    {
      label: 'Window',
      submenu: [
        { role: 'minimize' },
        { role: 'zoom' },
        ...(isMac ? [
          { type: 'separator' },
          { role: 'front' },
          { type: 'separator' },
          { role: 'window' }
        ] : [
          { role: 'close' }
        ])
      ]
    },
    {
      role: 'help',
      submenu: [
        {
          label: 'Learn More',
          click: async () => {
            const { shell } = require('electron')
            await shell.openExternal('https://electronjs.org')
          }
        }
      ]
    }
  ]

// Create browser window
let win
let login
function createWindows () {
    process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';
    win = new BrowserWindow({
        // Larger for DevTools
        width: 1400,
        height: 800,
        minWidth: 700,
        minHeight: 500,
        show: false,
        webPreferences: {
            nodeIntegration: true
        }
    });
    win.loadFile(path.join(__dirname, 'DayInReview/templates/home.html'));
    win.on('closed', () => {
      win = null;
    })

    login = new BrowserWindow({
        parent: win,
        width: 1000,
        height: 800,
        minWidth: 700,
        minHeight: 500,
        show: false,
        // frame: false,
        webPreferences: {
          nodeIntegration: true
        }
    });
    login.loadFile(path.join(__dirname, 'DayInReview/templates/login.html'));
    login.once('ready-to-show', () => {
      login.show();
    });
    login.on('close', () => {
      win.show();
    });
    login.on('closed', () => {
      login = null;
    });

    // Build Menu
    const mainMenu = Menu.buildFromTemplate(template);

    // Insert Menu
    Menu.setApplicationMenu(mainMenu);

    // Open with DevTools. 
    win.webContents.openDevTools() 

    return {
      main: win,
      login: login
    }
}

app.on('ready', () => {
  const {main, login} = createWindows();

  ipcMain.on('loginInfo', (event, arg) => {
    // Sends login info to main window
    main.webContents.send('loginInfo', arg);
  });
});

app.on('window-all-closed', () => {
  app.quit();
});
