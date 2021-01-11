#!C:\Python\Python38\python.exe
# Gmail API Python を使った認証方法
# https://typememo.jp/tech/gmail-api-authorize-with-python/

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES で、Gmail API に与える権限を定義します。
# 今回は、全てのリソースへの読み込みを許可します。
# SCOPES は readonly (読み込み許可) 意外にも modify (更新) や send (送信) など、様々なオプションがあります。
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Gmail API で認証する
def gmail_authorize():
    """Shows how to authorize Gmail API.
    """
    creds = None
    # The file token.pickle stores the user's access and
    # refresh tokens, and is created automatically when
    # the authorization flow completes for the first time.
    # まず、token.pickle というファイルがあるかどうか調べます。
    # もしも token.pickle ファイルがあれば、token.pickle ファイルをロードして、creds (credentials の略) に代入します。
    # token.pickle がなく、さらに、creds が有効ではない場合、creds を更新するようにリクエストをします。
    # token.pickle がなく、creds もなければ、credentials.json の情報に基づいて creds を発行し token.pickle を書き出します。
    # 最後に、creds を返して終了です。
    if os.path.exists('gmail_token.pickle'):
        with open('gmail_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('gmail_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main():
    """Shows the basic usage of Gmail API.
    1. Authorize Gmail API.
    """
    creds = gmail_authorize()
    service = build('gmail', 'v1', credentials=creds)
    print(creds)
    print(service)

if __name__ == '__main__':
    main()
