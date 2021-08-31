from django.db import models
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo

# Create your models here.
class pointHistory(models.Model):
    UserAccountInfo = models.ForeignKey("userlogin.UserAccountInfo", on_delete=models.CASCADE)
    modifier = models.CharField(verbose_name = "變更者" , max_length = 100)
    recordDate   = models.DateTimeField( verbose_name='修改日期')
    reason       = models.CharField(verbose_name = "原因" , max_length = 100)
    addPoint     = models.CharField(verbose_name = "增點" , max_length = 100)
    reducePoint  = models.CharField(verbose_name = "扣點" , max_length = 100)
    tranferPoint = models.CharField(verbose_name = "轉讓" , max_length = 100)
    resultPoint  = models.IntegerField( verbose_name='剩餘點數')

