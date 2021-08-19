from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from NutriliteSearchPage.models import personalFileData

import requests
logger = get_task_logger(__name__)

@shared_task
def getFileDateProcess(FileId,driveFileId,userName,fileType):
    my_data = {'fileId': driveFileId, 'userName': userName,'FileType':fileType}
    logger.info(f'{userName}')
    r = requests.post('http://127.0.0.1:9105/v1/getFile', data=my_data).text
    logger.info(f'{r}')
    d = personalFileData.objects.get(fileDataID=FileId)
    logger.info(d)
    d.waterCreateReady = 1
    d.waterMarkPath = r[2:]
    d.save()
#