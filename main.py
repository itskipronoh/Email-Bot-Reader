import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import oauth

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(sender, to, subject, message_text, user_id='me'):
    msg = create_message(sender, to, subject, message_text)
    try:
        service = oauth.get_g_service()
        message = (service.users().messages().send(userId=user_id, body=msg)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except ValueError as e:
        print('An error occurred: %s' % e)

def read_emails(user_id='me', max_results=5):
    try:
        service = oauth.get_g_service()
        results = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
        else:
            print('Messages:')
            for message in messages:
                msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
                headers = msg.get('payload', {}).get('headers', [])
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
                snippet = msg.get('snippet', 'No Snippet')
                print(f"Subject: {subject}")
                print(f"Snippet: {snippet}")
                print("-----")
    except ValueError as e:
        print('An error occurred: %s' % e)

# Example: Reading emails (prints subject and snippet of the latest 5 emails)
read_emails(user_id='me', max_results=5)


# Example: Sending a test email
send_message("user@example.com", "user@example.com", "test", "this is a test", user_id='me')

# Example: Reading emails (prints subject and snippet of the latest 5 emails)
read_emails(user_id='me', max_results=5)
