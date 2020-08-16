import csv
import os
import argparse
import imaplib
import email
import email.utils
import re
import joblib
import json
from bs4 import BeautifulSoup
from email.header import decode_header
from collections import Counter
from datetime import datetime
from extractive_summarizer import load_model as load_summary_model, get_summary


def get_links(email):
    return [a['href'] for a in email.find_all('a', href=True)]


def get_word_list():
    with open('keras/data/spam_filter_emails.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            return row[1:-1]


def get_word_counts(body):
    return Counter(body.split())


def load_model(model_name):
    return joblib.load(f'keras/models/{model_name}')


def remove_newlines(txt):
    txt = re.sub(r'[\r\n]+', '\n', txt)
    txt = re.sub(r'[\n\r]+', '\n', txt)
    txt = re.sub(r' +', ' ', txt)
    txt = re.sub(r'\n +', '\n', txt)
    txt = re.sub(r'\n+', '\n', txt)
    return txt


def get_email(imap, idx):
    res, message = imap.fetch(str(idx), "(RFC822)")
    for response in message:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            from_ = msg["From"]
            subject = msg["Subject"]
            date = email.utils.parsedate_to_datetime(msg["Date"])
            details = (from_, subject, date)

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        body = part.get_payload()
                    except:
                        return None, None, None
                    if content_type == 'text/plain':
                        remove_links = re.sub(r'http\S+', '', body)
                        return remove_newlines(remove_links), details, []
                    elif content_type == 'text/html':
                        soup = BeautifulSoup(body, features="html.parser")
                        links = get_links(soup)
                        for a in soup.findAll('a'):
                            a.replaceWithChildren()
                        return remove_newlines(soup.get_text()), details, links
            else:
                content_type = msg.get_content_type()
                try:
                    body = msg.get_payload()
                except:
                    return None, None, None
                if content_type == 'text/plain':
                    remove_links = re.sub(r'http\S+', '', body)
                    return remove_newlines(remove_links), details, []
                elif content_type == 'text/html':
                    soup = BeautifulSoup(body, features="html.parser")
                    links = get_links(soup)
                    for a in soup.findAll('a'):
                        a.replaceWithChildren()
                    return remove_newlines(soup.get_text()), details, links


def login(email, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        imap.login(email, password)
    except imaplib.IMAP4.error as e:
        exit(1)
    return imap


def logout(imap):
    imap.close()
    imap.logout()


def main():
    # Sets up parser
    parser = argparse.ArgumentParser(description='Classify emails for model training. Outputs a csv file formatted: [<message id>, <message body>, <class>]')
    parser.add_argument(
        '-e', '--email',
        dest='email',
        required=True,
        help='email address to look for emails'
    )
    parser.add_argument(
        '-p', '--password',
        dest='password',
        required=True,
        help='password for email account'
    )
    args = parser.parse_args()

    # Get wordlist
    word_list = get_word_list()

    # Login to email
    imap = login(args.email, args.password)

    # Loop through emails
    status, messages = imap.select("INBOX")
    num_messages = int(messages[0])
    if (num_messages == 0):
        exit(2)

    # Load model
    model = load_model('spam_filter_001.joblib')

    email_matrix = list()
    email_summaries = list()    # List to return
    for i in range(num_messages, 0, -1):
        body, details, links = get_email(imap, i)
        if body is None:
            continue
        if details[2].date() < datetime.today().date():
            print(json.dumps(dict((str(i), val) for (i, val) in enumerate(email_summaries))))
            break
        body = re.sub('[^A-Za-z \t\n,.]', '', body)
        word_counts = get_word_counts(body)
        
        # Add to email_matrix
        counts = list()
        for word in word_list:
            counts.append(word_counts[word])
        email_matrix.append(counts)

        # Prediction
        prediction = model.predict(email_matrix)[0]
        if prediction == 0:
            sender = details[0]
            if '\'' in sender or '\"' in sender:
                sender = sender.replace('\'', '')
                sender = sender.replace('\"', '')
            email_summaries.append({
                "from": sender,
                "subject": details[1],
                "date": str((details[2]).strftime("%B %d, %Y")),
                "time": str((details[2]).strftime("%-I:%M %p")),
                "links": json.dumps(dict((str(i), val) for (i, val) in enumerate(links))),
                "summary": get_summary(body)
            })
        email_matrix = list()

    # Logout of email
    logout(imap)


if __name__ == '__main__':
    load_summary_model()
    main()
