from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import base64
import os

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.file'
]

creds = Credentials.from_authorized_user_file('credentials.json', SCOPES)
gmail = build('gmail', 'v1', credentials=creds)
drive = build('drive', 'v3', credentials=creds)

messages = gmail.users().messages().list(userId='me', maxResults=1).execute().get('messages')
if not messages:
    print("No emails found")
    exit()

message = gmail.users().messages().get(userId='me', id=messages[0]['id']).execute()

print(message)

# attachments = []

# for part in message['payload'].get('parts', []):
#     filename = part.get('filename')
#     attachment_id = part.get('body', {}).get('attachmentId')
#     if filename and attachment_id:
#         data = gmail.users().messages().attachments().get(
#             userId='me', messageId=message['id'], id=attachment_id
#         ).execute()['data']
#         file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
#         with open(filename, 'wb') as f:
#             f.write(file_data)
#         attachments.append(filename)
#         print("Downloaded:", filename)

# for file_path in attachments:
#     drive.files().create(
#         body={'name': os.path.basename(file_path)},
#         media_body=MediaFileUpload(file_path),
#         fields='id'
#     ).execute()
#     print("Uploaded to Drive:", file_path)
