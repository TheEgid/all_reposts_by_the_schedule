from __future__ import print_function
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from urllib.parse import parse_qsl
from urlextract import URLExtract


def get_spreadsheet_values(spreadsheet_id, range_name):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                scopes=['https://spreadsheets.google.com/feeds'],
                client_secrets_file='credentials.json')
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name,
                                valueRenderOption='FORMULA').execute()
    values = result.get('values', [])
    if values:
        return values
    else:
        return None


def extract_file_id(row, column):
    _img_url = row[column]
    _img_url = URLExtract().find_urls(_img_url)[0]
    return parse_qsl(_img_url)[0][1]


if __name__ == '__main__':
    SPREADSHEET_ID = '17r4QRW_m0clut772bRnUL-U1-JiazImiZMm43SkgS9Q'
    RANGE_NAME = 'Лист1!A3:H100000'
    spreadsheet = get_spreadsheet_values(SPREADSHEET_ID, RANGE_NAME)

    txt_column = 5
    img_column = 6
    for row in spreadsheet:
        print(extract_file_id(row, txt_column))
        print(extract_file_id(row, img_column))