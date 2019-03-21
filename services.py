from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from urllib.parse import parse_qsl
from urlextract import URLExtract
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
    else:
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


def get_file_metadata_from_gdrive(file_id, credential_file='mycreds.txt'):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credential_file)
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile(credential_file)
    drive = GoogleDrive(gauth)
    my_file = drive.CreateFile({'id': file_id})
    if not file_id:
        return None
    else:
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
