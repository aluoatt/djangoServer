from django.db import models

# Create your models here.

class replayVideoInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='影片名稱')
    classRoom = models.CharField(max_length=50, verbose_name='所屬教室')
    uploadDate = models.DateTimeField(verbose_name='上傳日期')

