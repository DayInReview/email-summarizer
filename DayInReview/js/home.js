// loads content when the page is refreshed
window.onload = function() {
    loadHomePage(0);
    addRowHandlers();
}

// loads home page content
function loadHomePage(current_email) {
    var all_emails = Object.values(JSON.parse(localStorage.getItem('emails')));
    console.log(all_emails);

    document.getElementById("from").innerHTML = all_emails[current_email]['from'];
    document.getElementById("subject").innerHTML = all_emails[current_email]['subject'];
    document.getElementById("datetime").innerHTML = all_emails[current_email]['date'] + ' at ' + all_emails[current_email]['time'];
    document.getElementById("summary").innerHTML = all_emails[current_email]['summary'];
}
