#!C:\Python\Python38\python.exe

import urllib.request
import requests


def post_line(creds, send_message):
    """
    send message to LINE_notify
    Parameters
    ----------
    send_message:string
        string to send to LINE_notify
    Returns
    ---------
    """
    line_notify_token = creds
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': send_message}

    # create headers
    headers = {'Authorization': 'Bearer ' + line_notify_token}

    # send message
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)


def authorize_line(token_file):
    """Authorize LINE notify"""
    creds = None
    with open(token_file, encoding='utf-8') as token:
        #改行を取り除く
        creds = token.read().rstrip("\n")

    return creds
