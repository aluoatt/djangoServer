from django.db import models
from django.contrib.auth.models import User, AbstractUser  # 匯入 AbstractUser 類
from django.contrib.auth.hashers import make_password


# Create your models here.
class Server(models.Model):
    class Meta:
        permissions = (
            ("can_see_register", "can_see_register"),
            ("seeManagerMenuButton", "seeManagerMenuButton"),
            ("seeManagerAccountManagerPage", "seeManagerAccountManagerPage"),
            ("seeManagerAuditAccountPage", "seeManagerAuditAccountPage"),
            ("seeManagerPointPage", "seeManagerPointPage"),
            ("seeManagerArticlePage", "seeManagerArticlePage"),
            ("seeManagerStatisticPage", "seeManagerStatisticPage"),
            ("ALLAuditManager", "ALLAuditManager"),
            ("CYPManager", "CYPManager"),
            ("CYLManager", "CYLManager"),
            ("CYSManager", "CYSManager"),
            ("CYZManager", "CYZManager"),
            ("CYJManager", "CYJManager"),
            ("CYN2Manager", "CYN2Manager"),
            ("CYN1Manager", "CYN1Manager"),
            ("CYMManager", "CYMManager"),
            ("CYKManager", "CYKManager"),
            ("CYDManager", "CYDManager"),
            ("CYWManager", "CYWManager"),
            ("CYTManager", "CYTManager"),
            ("CYHManager", "CYHManager"),
            ("can_Change_DataPermission", "can_Change_DataPermission"),
            ("can_Change_JobTitle", "can_Change_JobTitle"),
            ("can_Change_class", "can_Change_class"),
            ("can_freeze_account", "can_freeze_account"),
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

    class Meta:
        verbose_name = "帳號管理"
        verbose_name_plural = "帳號管理"


class UserAccountAmwayInfo(models.Model):
    UserAccountInfo = models.ForeignKey("UserAccountInfo", on_delete=models.CASCADE, verbose_name='帳號')
    amwayNumber = models.IntegerField(verbose_name='會員編號')
    amwayAward = models.ForeignKey("amwayAwardInfo", on_delete=models.CASCADE, verbose_name='獎銜')
    amwayDD = models.ForeignKey("registerDDandDimInfo", verbose_name='白金', on_delete=models.PROTECT)

    # amwayDiamond = models.CharField(max_length=20, verbose_name='鑽石')
    class Meta:
        verbose_name = "帳號管理-安麗相關"
        verbose_name_plural = "帳號管理-安麗相關"


class UserAccountChainYenInfo(models.Model):
    UserAccountInfo = models.ForeignKey("UserAccountInfo", on_delete=models.CASCADE, verbose_name='帳號')
    jobTitle = models.ForeignKey("chainYenJobTitleInfo", on_delete=models.CASCADE, verbose_name='職務')
    classRoom = models.ForeignKey("chainYenClassInfo", on_delete=models.CASCADE, verbose_name='教室')
    # babysitter = models.CharField(max_length=20, verbose_name='保母')

    accountStatus = models.CharField(max_length=4, verbose_name='狀態')  # 停權
    freezeDate = models.DateTimeField(verbose_name='停權到期日', null=True,blank=True)
    point = models.IntegerField(verbose_name='點數')

    EM = models.BooleanField(verbose_name='愛馬')

    class Meta:
        verbose_name = "帳號管理-群雁相關"
        verbose_name_plural = "帳號管理-群雁相關"


class amwayAwardInfo(models.Model):
    rank = models.IntegerField()
    amwayAward = models.CharField(max_length=20, verbose_name='獎銜')

    class Meta:
        verbose_name = "獎銜資料表"
        verbose_name_plural = "獎銜資料表"

    def __str__(self):
        return self.amwayAward


class chainYenJobTitleInfo(models.Model):
    rank = models.IntegerField()
    jobTitle = models.CharField(max_length=20, verbose_name='職位')

    class Meta:
        verbose_name = "職位資料表"
        verbose_name_plural = "職位資料表"

    def __str__(self):
        return self.jobTitle


class chainYenClassInfo(models.Model):
    rank = models.IntegerField()
    ClassRoomName = models.CharField(max_length=20, verbose_name='教室名稱')
    ClassRoomCode = models.CharField(max_length=20, verbose_name='教室代碼')

    class Meta:
        verbose_name = "教室資料表"
        verbose_name_plural = "教室資料表"

    def __str__(self):
        return self.ClassRoomName


class registerDDandDimInfo(models.Model):
    amwayAward = models.ForeignKey("amwayAwardInfo", verbose_name='獎銜', on_delete=models.PROTECT)  # 只有白金跟鑽石
    amwayNumber = models.IntegerField(verbose_name='會員編號')
    amwayDiamond = models.CharField(max_length=20, verbose_name='上手鑽石')
    main = models.CharField(max_length=20, verbose_name='主直銷權')
    sec = models.CharField(max_length=20, verbose_name='次直銷權', null=True,blank=True)

    class Meta:
        verbose_name = "白金列表"
        verbose_name_plural = "白金列表"

    def __str__(self):
        return self.main


class TempUserAccountInfo(models.Model):
    """
    繼承 AbstractUser
    新增欄位：phone、addr
    """
    username = models.CharField(max_length=20, verbose_name='帳號')
    user = models.CharField(max_length=20, verbose_name='姓名')

    gender = models.CharField(max_length=4, verbose_name='性別')
    phone = models.CharField(max_length=50, verbose_name='電話')
    password = models.CharField(max_length=128, verbose_name='密碼')
    email = models.CharField(max_length=254, verbose_name='信箱')
    dataPermissionsLevel = models.IntegerField(verbose_name='資料權限等級')
    auditStatus = models.CharField(max_length=20, verbose_name='審核狀態')  # 審核中 #確認中

    class Meta:
        verbose_name = "註冊中帳號列表"
        verbose_name_plural = "註冊中帳號列表"
    def __str__(self):
        return self.username

class TempUserAccountAmwayInfo(models.Model):
    UserAccountInfo = models.ForeignKey("TempUserAccountInfo", on_delete=models.CASCADE,verbose_name='帳號')
    amwayNumber = models.IntegerField(verbose_name='會員編號')
    amwayAward = models.ForeignKey("amwayAwardInfo", on_delete=models.CASCADE, verbose_name='獎銜')
    amwayDD = models.ForeignKey("registerDDandDimInfo", verbose_name='白金', on_delete=models.PROTECT)
    # amwayDiamond = models.CharField(max_length=20, verbose_name='鑽石')
    class Meta:
        verbose_name = "註冊中帳號列表-安麗相關"
        verbose_name_plural = "註冊中帳號列表-安麗相關"

class TempUserAccountChainYenInfo(models.Model):
    UserAccountInfo = models.ForeignKey("TempUserAccountInfo", on_delete=models.CASCADE,verbose_name='帳號')
    jobTitle = models.ForeignKey("chainYenJobTitleInfo", on_delete=models.CASCADE, verbose_name='職務')
    classRoom = models.ForeignKey("chainYenClassInfo", on_delete=models.CASCADE, verbose_name='教室')
    # babysitter = models.CharField(max_length=20, verbose_name='保母')

    accountStatus = models.CharField(max_length=4, verbose_name='狀態')  # 停權
    freezeDate = models.DateTimeField(verbose_name='停權到期日', null=True,blank=True)
    point = models.IntegerField(verbose_name='點數')

    EM = models.BooleanField(verbose_name='愛馬')

    class Meta:
        verbose_name = "註冊中帳號列表-群雁相關"
        verbose_name_plural = "註冊中帳號列表-群雁相關"

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user_name = models.CharField(max_length=20, verbose_name='帳號')
    c_time = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.user.name + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "註冊確認碼"
        verbose_name_plural = "註冊確認碼"


# 修改紀錄
class AccountModifyHistory(models.Model):
    UserAccountInfo = models.ForeignKey("userlogin.UserAccountInfo", on_delete=models.CASCADE, verbose_name="被變更者")
    modifier = models.CharField(verbose_name="變更者", max_length=100)
    recordDate = models.DateTimeField(verbose_name='修改日期')
    modifyFielddName = models.CharField(verbose_name="變更欄位", max_length=100)
    originFieldData = models.CharField(verbose_name="原始值", max_length=255)
    RevisedData = models.CharField(verbose_name="變更後值", max_length=255)

    class Meta:
        verbose_name = "帳號更動歷史紀錄"
        verbose_name_plural = "帳號更動歷史紀錄"


class loginHistory(models.Model):
    user= models.ForeignKey(UserAccountInfo, on_delete=models.CASCADE,verbose_name="登入帳號")
    date= models.DateTimeField(auto_now_add= True,verbose_name="登入時間")
    ip = models.CharField(verbose_name="ip", max_length=100)

    class Meta:
        verbose_name = "登入紀錄"
        verbose_name_plural = "登入紀錄"

    def __str__(self):
        return str(self.user) + ': ' + str(self.date)