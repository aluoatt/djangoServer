from django.db import models

# Create your models here.

class replayVideoInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='影片名稱')
    classRoom = models.CharField(max_length=50, verbose_name='所屬教室')
    recordDate = models.DateTimeField(verbose_name='上傳日期')
    fileid = models.CharField(max_length=300, verbose_name='drive_fileid')

class confirmReplay(models.Model):
    title = models.CharField(max_length=50, verbose_name='影片名稱')
    videoSource = models.ForeignKey("replayVideoInfo",verbose_name='重播的影片',on_delete=models.PROTECT)
    confirmDate = models.DateTimeField(verbose_name='簽署日期')