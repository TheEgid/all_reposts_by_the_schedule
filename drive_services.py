from pydrive.auth import GoogleAuth
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials


def get_file(file_id, title):
    file_id = 'abc'
	file_access_token = '34244324324'
	scope = 'https://www.googleapis.com/auth/drive.readonly'
	path_to_private_key_file = '#'
	service_account_name = 'j35@developer.gserviceaccount.com'

	drive_client = GoogleDriveClient(
               scope = scope,
               private_key = open(path_to_private_key_file).read(),
               service_account_name = service_account_name)

	#file = drive_client.get_drive_file(file_id, file_access_token)


#https://github.com/MSF-Jarvis/pydrive-client/blob/master/main.py   
#http://qaru.site/questions/165781/automating-pydrive-verification-process
def drive_autorization():
    file_id = 'abc'
	gauth = GoogleAuth()
	# Try to load saved client credentials
	gauth.LoadCredentialsFile("mycreds.txt")
	if gauth.credentials is None:
		#gauth.LocalWebserverAuth()
		gauth.CommandLineAuth()
	elif gauth.access_token_expired:
		gauth.Refresh()
	else:
		gauth.Authorize()
	gauth.SaveCredentialsFile("mycreds.txt")

	
	drive = GoogleDrive(gauth)
	textfile = drive.CreateFile()
	textfile.SetContentFile('eng.txt')
	textfile.Upload()
	print (textfile)
	file_id = ''
	drive.CreateFile({'id':textfile['id']}).GetContentFile('eng-dl.txt')
	file = self.drive.CreateFile({'id': file_id})
	file.FetchMetadata()
	print(file.metadata["mimeType"])
	print(file.metadata["title"])
   
if __name__ == '__main__':
   drive_autorization()
   
