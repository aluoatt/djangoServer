from django.db import models
from django.contrib.auth.models import User, AbstractUser   # 匯入 AbstractUser 類

# Create your models here.
class Server(models.Model):

    class Meta:
        permissions = (
            ("can_see_register", "can_see_register"),
            ("seeManagerMenuButton","seeManagerMenuButton")
        )

class UserAccountInfo(AbstractUser):
    """
    繼承 AbstractUser
    新增欄位：phone、addr
    """
    user = models.CharField(max_length=20, verbose_name='姓名')

    gender = models.CharField(max_length=4, verbose_name='性別')
    phone = models.CharField(max_length=50, verbose_name='電話')
    dataPermissionsLevel = models.IntegerField(verbose_name='資料權限等級')

class UserAccountAmwayInfo(models.Model):
    UserAccountInfo = models.ForeignKey("UserAccountInfo",on_delete=models.CASCADE)
    amwayNumber = models.IntegerField()
    amwayAward = models.ForeignKey("amwayAwardInfo",on_delete=models.CASCADE, verbose_name='獎銜')
    amwayDD = models.ForeignKey("registerDDandDimInfo",verbose_name='白金',on_delete=models.PROTECT)
    # amwayDiamond = models.CharField(max_length=20, verbose_name='鑽石')

class UserAccountChainYenInfo(models.Model):
    UserAccountInfo = models.ForeignKey("UserAccountInfo",on_delete=models.CASCADE)
    jobTitle = models.ForeignKey("chainYenJobTitleInfo",on_delete=models.CASCADE, verbose_name='職務')
    classRoom = models.ForeignKey("chainYenClassInfo",on_delete=models.CASCADE, verbose_name='教室')
    # babysitter = models.CharField(max_length=20, verbose_name='保母')

    accountStatus = models.CharField(max_length=4, verbose_name='狀態') #停權
    freezeDate = models.DateTimeField( verbose_name='停權到期日',null=True)
    point = models.IntegerField( verbose_name='點數')

    EM = models.BooleanField(verbose_name='愛馬')

class amwayAwardInfo(models.Model):
    rank = models.IntegerField()
    amwayAward = models.CharField(max_length=20, verbose_name='獎銜')

class chainYenJobTitleInfo(models.Model):
    rank = models.IntegerField()
    jobTitle = models.CharField(max_length=20, verbose_name='職位')

class chainYenClassInfo(models.Model):
    rank = models.IntegerField()
    ClassRoomName = models.CharField(max_length=20, verbose_name='教室名稱')
    ClassRoomCode = models.CharField(max_length=20, verbose_name='教室代碼')

class registerDDandDimInfo(models.Model):
    amwayAward = models.ForeignKey("amwayAwardInfo", verbose_name='獎銜',on_delete=models.PROTECT)#只有白金跟鑽石
    amwayNumber = models.IntegerField( verbose_name='會員編號')
    amwayDiamond =models.CharField(max_length=20, verbose_name='上手鑽石')
    main = models.CharField(max_length=20, verbose_name='主直銷權')
    sec = models.CharField(max_length=20, verbose_name='次直銷權',null=True)



# from userlogin.models import amwayAwardInfo
# r = amwayAwardInfo.objects.create(rank=0,amwayAward="暫無")
# r = amwayAwardInfo.objects.create(rank=1,amwayAward="白金")
# r.save()

# r = chainYenClassInfo.objects.create(rank=0,ClassRoomName="台北",ClassRoomCode = "CYP")