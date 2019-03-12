
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#https://github.com/MSF-Jarvis/pydrive-client/blob/master/main.py   
#http://qaru.site/questions/165781/automating-pydrive-verification-process
def drive_autorization():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)

    file_id = '1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB'
    file = drive.CreateFile({'id': file_id})
    file.FetchMetadata()
    print(file.metadata['mimeType'])
    print(file.metadata['title'])
    print(file.metadata['webContentLink'])

    # print(
    #     'Downloading file %s from Google Drive' % file3['title'])


if __name__ == '__main__':
    drive_autorization()

