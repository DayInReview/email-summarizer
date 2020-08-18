// loads content when the page is refreshed
window.onload = function() {
    populateEmails();
    populateLinks(0);
    loadHomePage(0);
    addRowHandlers();
    persistentTable();
}

// populate the email sidebar with subjects and times
function populateEmails() {
    var all_emails = Object.values(JSON.parse(localStorage.getItem('emails')));
    var table = document.getElementById("email-table");
    
    for (var i = all_emails.length - 1; i >= 0; i--) {
        var email = all_emails[i];
        var row = table.insertRow(0);
        var subject_cell = row.insertCell(0);
        var datetime_cell = row.insertCell(1);

        subject_cell.innerHTML = email['subject'];
        datetime_cell.innerHTML = email['time'];
    }
}

// populate the links sidebar with links from the current email
function populateLinks(current_email) {
    var all_emails = Object.values(JSON.parse(localStorage.getItem('emails')));
    var email = all_emails[current_email];
    var links = JSON.parse(email['links']);
    var table = document.getElementById("links-table");
    table.innerHTML = "";

    for (var i = Object.keys(links).length - 1; i >= 0; i--) {
        var row = table.insertRow(0);
        var cell = row.insertCell(0);
        cell.innerHTML = `<a href=${links[i]}>Link ${i + 1}</a>`
    }
}

// loads home page content
function loadHomePage(current_email) {
    var all_emails = Object.values(JSON.parse(localStorage.getItem('emails')));
    // console.log(all_emails);
    var email = all_emails[current_email];

    document.getElementById("current-day").innerHTML = email['date'];
    document.getElementById("from").innerHTML = email['from'];
    document.getElementById("subject").innerHTML = email['subject'];
    document.getElementById("summary").innerHTML = email['summary'];
}
