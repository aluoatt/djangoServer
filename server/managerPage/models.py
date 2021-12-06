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

class blackList(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=100)
    gender = models.CharField(max_length=4, verbose_name='性別')
    phone = models.CharField(verbose_name="電話", max_length=100)
    amwayNumber = models.CharField(verbose_name="直銷商編號", max_length=100, null= True)
    id4 = models.CharField(verbose_name="身份證後四碼", max_length=100, null= True)

class blackRegisterRequest(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    id4 = models.CharField(max_length=20, verbose_name='身份證後四碼')
    amwayNumber = models.CharField(max_length=20, verbose_name='直銷商編號')
    gender = models.CharField(max_length=4, verbose_name='性別')
    phone = models.CharField(max_length=50, verbose_name='電話')
    email = models.CharField(max_length=254, verbose_name='信箱')
    ChainYenClass = models.CharField(max_length=254, verbose_name='教室')
    amwayDD = models.CharField(max_length=254, verbose_name='上手白金')
    amwayDiamond = models.CharField(max_length=254, verbose_name='上手鑽石')
    registerDate = models.DateTimeField(verbose_name='請求日期', auto_now = True)