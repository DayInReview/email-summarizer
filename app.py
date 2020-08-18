import csv
import os
import argparse
import imaplib
import email
import email.utils
import re
import joblib
import json
import quopri
from bs4 import BeautifulSoup
from email.header import decode_header
from collections import Counter
from datetime import datetime
from extractive_summarizer import load_model as load_summary_model, get_summary
from preprocessing import preprocess, remove_plain_text_special


def get_links(email):
    links = list()
    try:
        links = [a['href'] for a in email.find_all('a', href=True)]
    except:
        pass
    if links == []:
        try:
            links = [re.sub(r'[<>]', '', r) for r in re.findall(r'http\S+', email)]
        except:
            pass
    return links


def get_word_list():
    with open('keras/data/spam_filter_emails.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            return row[1:-1]


def get_word_counts(body):
    return Counter(body.split())


def load_model(model_name):
    return joblib.load(f'keras/models/{model_name}')


def get_email(imap, uid):
    res, message = imap.uid('fetch', str(uid), '(RFC822)')
    for response in message:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            from_ = msg["From"]
            subject = decode_header(msg["Subject"])[0][0]
            try:
                subject = subject.decode('utf-8')
            except:
                pass
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
                        return preprocess(body), details, get_links(body)
                    elif content_type == 'text/html':
                        try:
                            text = quopri.decodestring(body).decode('utf-8')
                        except:
                            text = body
                        soup = BeautifulSoup(text, features="html.parser")
                        links = get_links(BeautifulSoup(body, features="html.parser"))
                        for a in soup.findAll('a'):
                            a.replaceWithChildren()
                        return preprocess(soup.get_text()), details, links
            else:
                content_type = msg.get_content_type()
                try:
                    body = msg.get_payload()
                except:
                    return None, None, None
                if content_type == 'text/plain':
                    return preprocess(body), details, get_links(body)
                elif content_type == 'text/html':
                    try:
                        text = quopri.decodestring(body).decode('utf-8')
                    except:
                        text = body
                    soup = BeautifulSoup(text, features="html.parser")
                    links = get_links(BeautifulSoup(body, features="html.parser"))
                    for a in soup.findAll('a'):
                        a.replaceWithChildren()
                    return preprocess(soup.get_text()), details, links


def login(email, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        imap.login(email, password)
    except imaplib.IMAP4.error:
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
    imap.select("INBOX")
    status, messages = imap.uid('search', 'X-GM-RAW "category:primary"')
    messages = [int(m) for m in messages[0].decode().split()]
    messages.reverse()
    num_messages = len(messages)
    if (num_messages == 0):
        exit(2)

    # Load model
    # model = load_model('spam_filter_001.joblib')

    # email_matrix = list()
    email_summaries = list()    # List to return

    ct = 0
    for i in messages:
        ct += 1
        body, details, links = get_email(imap, i)
        if body is None:
            continue
        # word_counts = get_word_counts(body)
        
        # # Add to email_matrix
        # counts = list()
        # for word in word_list:
        #     counts.append(word_counts[word])
        # email_matrix.append(counts)

        # # Prediction
        # prediction = model.predict(email_matrix)[0]
        # if prediction == 0:
        sender = details[0]
        if '\'' in sender or '\"' in sender:
            sender = sender.replace('\'', '')
            sender = sender.replace('\"', '')
        email_summary = get_summary(body)
        if email_summary != "":
            email_summaries.append({
                "from": sender,
                "subject": details[1],
                "date": str((details[2]).strftime("%B %d, %Y")),
                "time": str((details[2]).strftime("%-I:%M %p")),
                "links": json.dumps(dict((str(i), val) for (i, val) in enumerate(links))),
                "summary": email_summary
            })
        # email_matrix = list()
        
        # check if email is before current day or there are no more emails
        if details[2].date() < datetime.today().date() or ct == num_messages:
            print(json.dumps(dict((str(i), val) for (i, val) in enumerate(email_summaries))))
            break

    # Logout of email
    logout(imap)


if __name__ == '__main__':
    load_summary_model()
    main()
