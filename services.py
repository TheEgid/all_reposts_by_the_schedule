from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from urllib.parse import parse_qsl
from urlextract import URLExtract
import logging
import requests
import os
import re


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


def save_files(url, filename, dir_name='content_folder/'):
    filepath = dir_name+filename
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, 'wb') as f:
        f.write(response.content)
        logging.info('download & saved {}'.format(filepath))



# https://github.com/MSF-Jarvis/pydrive-client/blob/master/main.py
# http://qaru.site/questions/165781/automating-pydrive-verification-process

def get_file_metadata_from_gdrive(file_id, credential_file='mycreds.txt'):
    logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.INFO)
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
    myfile = drive.CreateFile({'id': file_id})
    myfile.FetchMetadata()
    if myfile.metadata['mimeType'] == 'application/vnd.google-apps.document':
        metadata_dict = {
            'file_link': myfile.metadata['exportLinks']['text/plain'],
            'file_title': '{}.txt'.format(myfile.metadata['title'])
        }
    elif myfile.metadata['mimeType'] == 'image/jpeg':
        metadata_dict = {
            'file_link': myfile.metadata['webContentLink'],
            'file_title': myfile.metadata['title']
        }
    else:
        return None
    return metadata_dict





