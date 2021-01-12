#!C:\Python\Python38\python.exe
# Gmail API Python メッセージとスレッドの取得方法
# https://typememo.jp/tech/gmail-api-get-messages-and-threads-with-python/

import base64
import os.path
import pickle
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def authorize(SCOPES, token_file, credentials_file):
    """Authorize Gmail API."""
    creds = None
    # The file token.pickle stores the user's access and
    # refresh tokens, and is created automatically when
    # the authorization flow completes for the first time.
    if os.path.exists(token_file):
        with open("gmail_token.pickle", 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return creds


def build_service(creds):
    """Build Gmail API."""
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_messages(service, userid="me", query="", maxResults=100):
    """Get messages list."""
    msgs_list = service.users().messages().list(
        userId=userid,
        q=query,
        maxResults=maxResults,
    ).execute().get('messages')
    return msgs_list


def get_message(service, message, userid="me"):
    """Get a message."""
    msg = service.users().messages().get(
        userId=userid,
        id=message['id']
    ).execute()
    return msg


def get_message_from(message):
    """Get sender of message"""
    headers = get_message_headers(message)
    for header in headers:
        if header["name"] == "From":
            msg_from = header["value"]
            return msg_from
    print("Not found subject")
    return None


def get_message_subject(message):
    """Get message subject."""
    headers = get_message_headers(message)
    for header in headers:
        if (header["name"] == "Subject"):
            subject = header["value"]
            return subject
    print("Not found subject")
    return None


def get_message_body(message):
    """Get message body."""
    part = get_message_part(message)
    try:
        body = part["body"]["data"]
    # except TypeError:
    except KeyError:
        # 通常はpart["body"]["data"]で読めるが、読めない場合は下記とする
        body = part["parts"][0]["parts"][0]["parts"][1]["body"]["data"]
    finally:
        return body


def get_message_part(message):
    """Get message part."""
    message_part = message["payload"]
    return message_part


def get_message_headers(message):
    """Get headers from message."""
    headers = message["payload"]["headers"]
    return headers


def decode(encoded):
    """Decode message body."""
    decoded = base64.urlsafe_b64decode(encoded).decode()
    return decoded


def get_threads(service, userid="me", query=""):
    """Get messages list."""
    threads_list = service.users().threads().list(
        userId=userid,
        q=query
    ).execute().get('threads')
    return threads_list


def get_thread(service, thread, userid="me"):
    """Get a message."""
    thread = service.users().threads().get(
        userId=userid,
        id=thread['id']
    ).execute()
    return thread


def remove_label_from_message(service, labelslist, message, userid="me"):
    """Remove label from message"""
    labels = {"removeLabelIds": labelslist}
    service.users().messages().modify(
        userId=userid,
        id=message["id"],
        body=labels,
    ).execute()


def send_message(service, To, From, subject, body, user_id="me"):
    """Send a message"""
    send_message = MIMEText(body)
    send_message["to"] = To
    send_message["from"] = From
    send_message["subject"] = subject
    service.users().messages().send(
        userId=user_id, body={
            "raw": base64.urlsafe_b64encode(
                send_message.as_bytes()).decode()}).execute()
