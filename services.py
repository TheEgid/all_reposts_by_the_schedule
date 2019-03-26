from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError
from urllib.parse import parse_qsl
from urlextract import URLExtract
import pickle
import argparse
import logging
import requests
import os
import re


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', default="all", type=str,
                        help='valid commands only: hh, sj, all')
    return parser


def create_google_color(r, g, b):
    red = 255-r
    green = 255-g
    blue = 255-b
    if red == 0:
        red = 1.0
    if green == 0:
        green = 1.0
    if blue == 0:
        blue = 1.0
    color = {'red': red, 'green': green, 'blue': blue}
    return color


def extract_google_spreadsheet_id(_string):
    regex = r'[^d/][A-Za-z0-9_-]{20,}'
    spreadsheet_id = re.findall(regex, _string)
    if not spreadsheet_id:
        return None
    return spreadsheet_id[0]


def extract_file_id(text):
    try:
        _text = URLExtract().find_urls(str(text))[0]
        return parse_qsl(_text)[0][1]
    except IndexError:
        return None


def download_and_save_file(url, filename, number, dir_name='content_folder'):
    filepath = \
        os.path.join(dir_name, str(number) + os.path.splitext(filename)[-1])
    os.makedirs(dir_name, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'wb') as f:
        f.write(response.content)
        logging.info(' Downloaded & saved {}'.format(filepath))


def get_file_metadata_from_gdrive(service, file_id):
    try:
        my_file = service.CreateFile({'id': file_id})
        my_file.FetchMetadata()
        if my_file.metadata['mimeType'] == 'application/vnd.google-apps.document':
            metadata_dict = {
                'file_link': my_file.metadata['exportLinks']['text/plain'],
                'file_title': '{}.txt'.format(my_file.metadata['title'])
            }
        elif my_file.metadata['mimeType'] == 'image/jpeg':
            metadata_dict = {
                'file_link': my_file.metadata['webContentLink'],
                'file_title': my_file.metadata['title']
            }
        else:
            return None
        return metadata_dict
    except ApiRequestError:
        raise TypeError('wrong file_id')


def authorize_google_drive(credential_file='mycreds.txt'):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credential_file)
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile(credential_file)
    drive_service = GoogleDrive(gauth)
    return drive_service


def authorize_google_spreadsheets():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
                client_secrets_file='client_secrets.json')
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    return service


def read_spreadsheet_range(service, link, range):
    spreadsheet_id = extract_google_spreadsheet_id(link)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range,
                                valueRenderOption='FORMULA').execute()
    return result.get('values', [])


def write_spreadsheet_cell(service, link, cell_address=None):
    spreadsheet_id = extract_google_spreadsheet_id(link)
    row, column = cell_address
    requests = [{'repeatCell': {
        'range': {'sheetId': 0, 'startRowIndex': row-1, 'endRowIndex': row,
                  'startColumnIndex': column-1, 'endColumnIndex': column},
        'cell': {'userEnteredValue': {'stringValue': 'да'}, #да
                 'userEnteredFormat': {
                     'backgroundColor': create_google_color(217, 234, 211)}},
        'fields': 'userEnteredValue,userEnteredFormat(backgroundColor)'}}]
    body = {'requests': requests}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                       body=body).execute()