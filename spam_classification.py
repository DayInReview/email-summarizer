import csv
import os
import argparse
import imaplib
import email
import re
import joblib
from bs4 import BeautifulSoup
from email.header import decode_header
from collections import Counter
from extractive_summarizer import load_model as load_summary_model, get_summary


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
            message_id = decode_header(msg["Message-ID"])[0][0]

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == 'text/plain':
                        remove_links = re.sub(r'http\S+', '', body)
                        return remove_newlines(remove_links), message_id
                    elif content_type == 'text/html':
                        soup = BeautifulSoup(body, features="html.parser")
                        for a in soup.findAll('a'):
                            a.replaceWithChildren()
                        return remove_newlines(soup.get_text('\n')), message_id
            else:
                content_type = msg.get_content_type()
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    return None, None
                if content_type == 'text/plain':
                    remove_links = re.sub(r'http\S+', '', body)
                    return remove_newlines(remove_links), message_id
                elif content_type == 'text/html':
                    soup = BeautifulSoup(body, features="html.parser")
                    for a in soup.findAll('a'):
                        a.replaceWithChildren()
                    return remove_newlines(soup.get_text('\n')), message_id


def login(email, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(email, password)
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

    # Load model
    model = load_model('spam_filter_001.joblib')

    email_matrix = list()
    for i in range(num_messages, 0, -1):
        body, message_id = get_email(imap, i)
        if body is None:
            continue
        body = re.sub('[^A-Za-z \t\n,.]', '', body)
        word_counts = get_word_counts(body)
        
        # Add to email_matrix
        counts = list()
        for word in word_list:
            counts.append(word_counts[word])
        email_matrix.append(counts)

        print('==================================================')
        print(body)
        print()

        # Prediction
        prediction = model.predict(email_matrix)[0]
        if prediction == 1:
            print('SPAM')
        else:
            print('NOT SPAM')
            print('Summary: ')
            print(get_summary(body))

        response = input('Continue? (y/n) ')
        if response != 'y':
            break
        email_matrix = list()

    # Logout of email
    logout(imap)


if __name__ == '__main__':
    load_summary_model()
    main()
