from django.db import models

# Create your models here.

class rewardReport(models.Model):
    reporter      = models.ForeignKey('userlogin.UserAccountInfo', related_name="rewardReporter", on_delete=models.CASCADE, verbose_name='請求者')
    handler       = models.ForeignKey('userlogin.UserAccountInfo', related_name="rewardHandler", on_delete=models.CASCADE, verbose_name='處理者', null=True)
    reason        = models.CharField(max_length=50, verbose_name='獎賞原因')
    rewardList    = models.CharField(max_length=1000, verbose_name='獎賞名單')
    status        = models.CharField(max_length=50, verbose_name='狀態') #待處理report/已完成finish/無效回報discard
    discardReason = models.CharField(max_length=50, verbose_name='無效原因', null= True)
    recordDate    = models.DateTimeField(verbose_name='請求日期')
    handleDate    = models.DateTimeField(verbose_name='處理日期', null=True)
