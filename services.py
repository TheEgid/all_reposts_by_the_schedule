from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from urllib.parse import parse_qsl
from urlextract import URLExtract
import requests
import os
import re


def extract_google_spreadsheet_id(_string):
    regex = r'[^d/][A-Za-z0-9_]{20,}'
    spreadsheet_id = re.findall(regex, _string)
    if not spreadsheet_id:
        return None
    else:
        return spreadsheet_id[0]


def extract_file_id(text):
    text= str(text)
    try:
        _text = URLExtract().find_urls(text)[0]
        return parse_qsl(_text)[0][1]
    except IndexError:
        return None


# https://github.com/MSF-Jarvis/pydrive-client/blob/master/main.py
# http://qaru.site/questions/165781/automating-pydrive-verification-process
def save_file(url, filename, dir_name='content_folder/'):
    filepath = dir_name+filename
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    response = requests.get(url)
    if response.ok:
        with open(filepath, 'wb') as f:
            f.write(response.content)
            # logging.info('download & saved ' + filename)
        # make_imageresize(filename, extension)
    else:
        return None


def get_file_metadata_from_gdrive(file_id, credential_file="mycreds.txt"):
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




if __name__ == '__main__':
    #file_id = '1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH'

    r = ['18uujc6MSE-byyAHKQHo_E9mA3Hdhsfu3kPXd9A3NcaQ', '1gsNyLmQvCmTqWV9WRw7exTnK31BPg-4i']

    for el in r:
        print(get_file_metadata_from_gdrive(el))
        data = get_file_metadata_from_gdrive(el)

        save_file(data['file_link'], data['file_title'])

