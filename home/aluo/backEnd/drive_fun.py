from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload
import io
class googleDriveDownload():
    def __init__(self,logger):
        self.logger = logger
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    def downloadFile(self,id,outputFileName,FileType='pdf'):
        file_id = id
        request = self.DRIVE.files().get_media(fileId=file_id)
        # fh = io.BytesIO()
        fh = io.FileIO(outputFileName+"." +FileType, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        self.logger.info("Download " + id + " start")
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        self.logger.info("Download " + id + " success")

# if __name__ == '__main__':
#     n = googleDriveDownload(3)

