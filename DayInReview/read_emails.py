import imaplib
import email
from email.header import decode_header
import webbrowser
import os

def read_emails(username, password, N):
    # Create IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    num_messages = int(messages[0])

    for i in range(num_messages, num_messages-N, -1):
        print("==============================================")
        res, message = imap.fetch(str(i), "(RFC822)")
        for response in message:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                from_ = msg.get("From")
                print(f"Subject: {subject}")
                print(f"From: {from_}")

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == 'text/plain':
                            print(body)
                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if content_type == 'text/plain':
                        print(body)

    imap.close()
    imap.logout()

if __name__ == '__main__':
    username = input("Enter email: ")
    password = input("Enter password: ")
    N = int(input("How many emails? "))
    read_emails(username, password, N)
