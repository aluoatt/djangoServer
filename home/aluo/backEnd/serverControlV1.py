from core.addWaterMark import create_PDF_water,create_mp4_water,create_PDF_without_water

import os
from drive_fun import googleDriveDownload


class ServerControlV1(object):
    def __init__(self, logger):
        self.googleDriveDownload = googleDriveDownload(logger)
        pass

    def checkFielExist(self, target_file):

        if os.path.exists(target_file+'.mp4'):
            print(target_file+'.mp4' + '檔案存在')
            return True, target_file+'.mp4'

        elif os.path.exists(target_file+'.pdf'):
            print(target_file + '.pdf' + '檔案存在')
            return True, target_file + '.pdf'
        else:
            print(target_file+'.mp4' + '不存在')
            return False, ""

    def downloadFileFromDrive(self, fileId, userName, FileType):
        os.makedirs('./personalData/' + userName, exist_ok=True)

        self.googleDriveDownload.downloadFile(id=fileId, outputFileName='./personalData/' + userName + '/' + fileId, FileType=FileType)

    def downloadFileFromDriveWithOutWater(self, fileId, userName, FileType):

        print("fileId::",fileId)
        os.makedirs('./personalData/' + userName, exist_ok=True)
        self.googleDriveDownload.downloadFile(id=fileId, outputFileName='./personalData/' + userName + '/' + fileId+"_"+userName, FileType=FileType)

    # return file path
    def getFileWithWaterMark(self, fileId, userName, FileType="pdf"):
        target_file_path = './personalData/' + userName + '/' + fileId
        fileExist, fileWithWater = self.checkFielExist(target_file_path + "_" + userName)

        if fileExist:
            return fileWithWater

        self.downloadFileFromDrive(fileId=fileId, userName=userName, FileType=FileType)

        if FileType == "pdf":
            create_PDF_water(username=userName, rawPDFPath=target_file_path+"." + FileType, outputPDFPath=target_file_path+"_"+userName + '.pdf')
            os.remove(target_file_path+"." + FileType)
            return target_file_path+"_"+userName + '.pdf'

        if FileType == "mp4":
            create_mp4_water(userName,target_file_path+'.mp4',outputVideoPath=target_file_path+"_"+userName + '.mp4')
            os.remove(target_file_path + "." + FileType)
            return target_file_path + "_" + userName + '.mp4'

    def getFileWithoutWaterMark(self, fileId, userName, FileType="pdf"):

        target_file_path = './personalData/' + userName + '/' + fileId
        if FileType == "pdf":
            self.downloadFileFromDrive(fileId=fileId, userName=userName, FileType=FileType)
            create_PDF_without_water(username=userName, rawPDFPath=target_file_path + "." + FileType,
                                     outputPDFPath=target_file_path + "_" + userName + '.pdf')
            return target_file_path + "_" + userName + '.pdf'

        if FileType == "mp4":
            self.downloadFileFromDriveWithOutWater(fileId=fileId, userName=userName, FileType=FileType)
            return target_file_path + "_" + userName + '.mp4'
