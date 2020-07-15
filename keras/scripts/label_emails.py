import csv
import argparse
import imaplib
import email
from email.header import decode_header


def write_to_csv(filepath, message_id, body, class_):
    with open(filepath, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([message_id, body, class_])


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
                        return body, message_id
            else:
                content_type = msg.get_content_type()
                body = msg.get_payload(decode=True).decode()
                if content_type == 'text/plain':
                    return body, message_id


def login(email, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(email, password)
    return imap


def logout(imap):
    imap.close()
    imap.logout()


def check_unique(message_id, filepath):
    emails = list()
    with open(filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            emails.append(row)
    id_list = [email[0] for email in emails]
    if message_id in id_list:
        return False
    else:
        return True


def main():
    # Sets up parser
    parser = argparse.ArgumentParser(description='Classify emails for model training. Outputs a csv file formatted: [<message body>, <class>]')
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
    parser.add_argument(
        '-f', '--filepath',
        dest='filepath',
        required=True,
        help='filepath for output csv'
    )
    parser.add_argument(
        '-c', '--classes',
        nargs='+',
        dest='classes',
        required=True,
        help='classes for labeling the emails'
    )
    args = parser.parse_args()
    classes = dict(enumerate(args.classes))

    # Login to email
    imap = login(args.email, args.password)

    # Loop through emails
    status, messages = imap.select("INBOX")
    num_messages = int(messages[0])

    for i in range(num_messages, 0, -1):
        body, message_id = get_email(imap, i)
        if check_unique(message_id, args.filepath):
            print('==================================================')
            print(body)
            print(classes)
            class_ = int(input('What is the classification? '))
            while class_ not in classes.values():
                print('Invalid class')
                class_ = int(input('What is the classification? '))
            write_to_csv(args.filepath, message_id, body, class_)

    # Logout of email
    logout(imap)


if __name__ == '__main__':
    main()
    # check_unique('test', 'keras/data/labeled_emails.csv')
