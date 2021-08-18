from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger

import requests
logger = get_task_logger(__name__)

@shared_task
def getFileDateProcess(FileId,userName,fileType):
    my_data = {'fileId': FileId, 'userName': userName,'FileType':FileType}
    print(userName)
    logger.info(f'{userName}')
    r = requests.post('http://127.0.0.1:9105/v1/getFile', data=my_data).text
    logger.info(f'{r}')
    print(r)