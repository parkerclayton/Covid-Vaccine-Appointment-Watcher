"""
These methods taken from Gmail's API quickstart docs
https://developers.google.com/gmail/api/quickstart/python

"""

from googleapiclient.discovery import build
import pickle
from email.mime.text import MIMEText
import base64
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class MailClient(object):
    """
    Basic mail client wrapper for the gmail api
    """

    def __init__(self, token_file='token.pickle'):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
        self.service = build('gmail', 'v1', credentials=creds)

    @staticmethod
    def create_message(sender, to, subject, message_text):
        """Create a message for an email.

        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw.decode()}

    def send_message(self, sender_email, recipient_email, subject, message_text):
        """Send an email message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

        Returns:
            Sent Message.
        """
        message = self.create_message(sender_email, recipient_email, subject, message_text)

        try:
            message = (self.service.users().messages().send(userId='me', body=message)
                    .execute())
            print('Message Id: %s' % message['id'])
            return message
        except Exception as error:
            print('An error occurred: %s' % error)

    def send_multiple_emails(self, messages_dict):
        for message in messages_dict:
            self.send_message(message['from'], message['to'], message['subject'], message['body'])

def generate_gmail_token(creds_path='credentials.json'):
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        if not os.path.exists(creds_path):
            print('ERROR - unable fo find {}.' \
            'Please download from: https://developers.google.com/gmail/api/quickstart/python'.format(creds_path))
            return False

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return True
