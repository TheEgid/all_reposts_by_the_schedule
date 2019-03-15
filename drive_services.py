from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#https://github.com/MSF-Jarvis/pydrive-client/blob/master/main.py   
#http://qaru.site/questions/165781/automating-pydrive-verification-process



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
  file_metadata = {file_type: file.metadata['mimeType'], file_tittle: file.metadata['title'], file_link: file.metadata['webContentLink']}
  return file_metadata


if __name__ == '__main__':
  file_id = '1yKE3DsV3ya0YzTpWDKH4sUxPo_4BMauB'
  print(get_file_metadata_from_gdrive(file_id))
