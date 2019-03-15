from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import requests
import os

# https://github.com/MSF-Jarvis/pydrive-client/blob/master/main.py
# http://qaru.site/questions/165781/automating-pydrive-verification-process


def save_file(url, filename, dir_name='images/'):
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

    r = ['1Wthk5k2ucVXpsa_J2F9TTflA2ztjcarLu81Rtb05ps8',
         '1zljULNgX1h1sS9x4iWLaDZQEVEMNf5PH']

    for el in r:
        print(get_file_metadata_from_gdrive(el))
        data = get_file_metadata_from_gdrive(el)

        save_file(data['file_link'], data['file_title'])

