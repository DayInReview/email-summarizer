# Day in Review
A desktop email client that uses extractive summarization to make it easier to read through your emails. Built with Electron JS and Python.

## Contributors
- Rishi Ponnekanti
- Ishan Shah

## Installation Guide

### Clone the Project
Clone this project into your working directory with this command.
```bash
git clone https://github.com/ishan0102/day-in-review.git
```

### Python Dependencies
Install the Python modules used in this project. Must have Python 3.6 or higher.
```bash
python -m pip install -r requirements.txt
```

### Node and NPM
Check to see if you have Node and Node Package Manager (NPM) installed.
```bash
node -v # check node version
npm -v # check npm version
```
If both of those returned version numbers, you can skip to [`NPM Install`](#npm-install). Otherwise, follow along to install what you're missing.

#### Node.js
You can get the Node.js installer for your system using [this link](https://nodejs.org/en/download/).

#### NPM
You can install NPM from the command line with this command.
```bash
npm install npm@latest -g # install latest version of npm
```

### NPM Install
The next step is to install the necessary `node_modules` for your system. This can be done from the command line as well. **Make sure you're in the project directory.**
```bash
npm install # install node modules
```

### NPM Start
Finally, run the desktop app locally. This is done with Electron.
```bash
npm start # runs the application
```