from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from NutriliteSearchPage.models import personalFileData
import datetime
import requests

logger = get_task_logger(__name__)

@shared_task
def getReplayVideoProcess(FileId, driveFileId, userName, fileType, ownerAccountId):
    my_data = {'fileId': driveFileId, 'userName': userName, 'FileType': fileType}
    logger.info(f'{userName}')
    r = requests.post('http://127.0.0.1:9104/v1/getReplayVideoProcess', data=my_data).text
    logger.info(f'{r}')
    d = personalFileData.objects.filter(fileDataID=FileId, ownerAccount=ownerAccountId).first()
    logger.info(d)
    d.waterCreateReady = 1
    d.create_Date_E=str(datetime.datetime.now())
    d.waterMarkPath = r[2:]
    d.save()
