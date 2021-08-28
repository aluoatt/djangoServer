import time
# 这个Celery就类似于flask中的Flask, 然后实例化得到一个app
from celery import Celery
import requests

# 指定一个name、以及broker的地址、backend的地址
app = Celery("satori",
             broker="redis://localhost:6379/1",
             backend="redis://localhost:6379/2")


# 这里通过@app.task对函数进行装饰，那么之后我们便可通过调用task.delay创建一个任务
@app.task
def getFileProcess(fileId, userName,fileType):
    print(userName + "開始取得檔案")


    return f" {fileId},type:{fileType} - {userName} is ready"