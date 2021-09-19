from django.db import models
from django.utils import timezone


class fileDataInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='標題')
    mainClass = models.ForeignKey("mainClassInfo",verbose_name='主類別',on_delete=models.PROTECT)
    secClass = models.ForeignKey("secClassInfo",verbose_name = '次類別',on_delete=models.PROTECT)
    describe = models.CharField(max_length=500, verbose_name='描述')
    PDF = models.CharField(max_length=255,verbose_name='PDF路徑',null=True,blank=True)
    file = models.CharField(max_length=255,verbose_name='file路徑')
    fileType = models.ForeignKey("fileTypeInfo",verbose_name='檔案格式',on_delete=models.PROTECT)
    sourceFrom = models.ForeignKey("sourceFromInfo",verbose_name='資料來源',on_delete=models.PROTECT)
    sourceURL = models.CharField(max_length=255,verbose_name='來源網址',null=True,blank=True)
    sourceScreenshot = models.CharField(max_length=255,verbose_name='來源示意圖路徑',null=True,blank=True)
    characterName = models.CharField(max_length=20,verbose_name='421主角姓名',null=True,blank=True)
    characterClass = models.ForeignKey("userlogin.chainYenClassInfo",verbose_name='421主角歸屬教室',null=True,blank=True,on_delete=models.PROTECT)
    characterDD = models.CharField(max_length=20,verbose_name='421主角上手白金',null=True,blank=True)
    occurrenceDate = models.DateTimeField(verbose_name='資料發生日期')
    lastModify = models.DateTimeField(verbose_name='資料修改日期')
    visible = models.BooleanField(verbose_name='是否可見')
    needWaterMark = models.BooleanField(verbose_name='是否需要浮水印')
    point = models.IntegerField(verbose_name='耗費點數')
    permissionsLevel = models.IntegerField(verbose_name='權限等級')
    DBClass = models.ForeignKey("DBClassInfo",verbose_name='資料庫類別',on_delete=models.PROTECT)
    downloadAble = models.BooleanField(verbose_name='是否可以下載')
    likes = models.IntegerField(default=0,verbose_name="按讚數")

    class Meta:
        verbose_name = "檔案管理"
        verbose_name_plural = "檔案管理"

    def __str__(self):
        return self.title
#資料庫類別對應表
class DBClassInfo(models.Model):

    DBClassName = models.CharField(max_length=100,verbose_name='名稱')
    DBClassCode = models.CharField(max_length=50,verbose_name='編碼')
    def __str__(self):
        return self.DBClassCode

    class Meta:
        verbose_name = "資料庫類別對應表(C.A.O)"
        verbose_name_plural = "資料庫類別對應表(C.A.O)"

#主類別對應表
class mainClassInfo(models.Model):

    mainClassName = models.CharField(max_length=50,verbose_name='主類別名稱',null=True,blank=True)
    def __str__(self):
        return self.mainClassName
    class Meta:
        verbose_name = "主類別對應表"
        verbose_name_plural = "主類別對應表"

#次類別對應表
class secClassInfo(models.Model):
    secClassName = models.CharField(max_length=50, verbose_name='主類別名稱', null=True,blank=True)
    def __str__(self):
        return self.secClassName
    class Meta:
        verbose_name = "次類別對應表"
        verbose_name_plural = "次類別對應表"
#檔案類型對應表
class fileTypeInfo(models.Model):

    fileTypeName = models.CharField(max_length=50,verbose_name='檔案類型對應表',null=True,blank=True)
    def __str__(self):
        return self.fileTypeName
    class Meta:
        verbose_name = "檔案類型對應表"
        verbose_name_plural = "檔案類型對應表"
#資料來源對應表
class sourceFromInfo(models.Model):
    sourceFromName = models.CharField(max_length=50, verbose_name='資料來源名稱', null=True,blank=True)
    def __str__(self):
        return self.sourceFromName
    class Meta:
        verbose_name = "資料來源對應表"
        verbose_name_plural = "資料來源對應表"

class fileDataKeywords(models.Model):
    fileDataInfoID = models.ForeignKey('fileDataInfo',verbose_name='對應的資料ID',on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, verbose_name='關鍵字名稱', null=True,blank=True)
    class Meta:
        verbose_name = "檔案關鍵字"
        verbose_name_plural = "檔案關鍵字"

#個人持有資料
class personalFileData(models.Model):
    fileDataID = models.ForeignKey('fileDataInfo',on_delete=models.CASCADE,verbose_name='對應的資料')
    ownerAccount = models.ForeignKey('userlogin.UserAccountInfo',on_delete=models.CASCADE,verbose_name='對應的帳號')
    exchangeDate = models.DateTimeField(verbose_name='資料兌換日期')
    expiryDate = models.DateField(verbose_name='資料兌換時效到期日',null=True,blank=True)
    costPoint = models.IntegerField(verbose_name='花費點數')
    waterCreateReady = models.BooleanField(default=0,verbose_name='浮水印是否完成')
    waterMarkPath = models.CharField(max_length=400,verbose_name='浮水印檔案路徑', null=True,blank=True)
    like = models.BooleanField(default=0,verbose_name='是否按讚')
    class Meta:
        verbose_name = "個人持有資料管理"
        verbose_name_plural = "個人持有資料管理"
class personalExchangeFileLog(models.Model):
    fileDataID = models.ForeignKey('fileDataInfo', on_delete=models.CASCADE, verbose_name='對應的資料')
    ownerAccount = models.ForeignKey('userlogin.UserAccountInfo', on_delete=models.CASCADE, verbose_name='對應的帳號')
    exchangeDate = models.DateTimeField(verbose_name='資料兌換日期',default=timezone.now)
    costPoint = models.IntegerField(verbose_name='花費點數')
    class Meta:
        verbose_name = "個人兌換紀錄"
        verbose_name_plural = "個人兌換紀錄"
