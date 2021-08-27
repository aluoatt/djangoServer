from django.db import models
from django.utils import timezone
# Create your models here.


class fileDataInfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='標題')
    mainClass = models.ForeignKey("mainClassInfo",verbose_name='主類別',on_delete=models.PROTECT)
    secClass = models.ForeignKey("secClassInfo",verbose_name = '次類別',on_delete=models.PROTECT)
    describe = models.CharField(max_length=500, verbose_name='描述')
    PDF = models.CharField(max_length=255,verbose_name='PDF路徑',null=True)
    file = models.CharField(max_length=255,verbose_name='file路徑')
    fileType = models.ForeignKey("fileTypeInfo",verbose_name='檔案格式',on_delete=models.PROTECT)
    sourceForm = models.ForeignKey("sourceFromInfo",verbose_name='資料來源',on_delete=models.PROTECT)
    sourceURL = models.CharField(max_length=255,verbose_name='來源網址',null=True)
    sourceScreenshot = models.CharField(max_length=255,verbose_name='來源示意圖路徑',null=True)
    characterName = models.CharField(max_length=20,verbose_name='421主角姓名',null=True)
    characterClass = models.ForeignKey("userlogin.chainYenClassInfo",verbose_name='421主角歸屬教室',null=True,on_delete=models.PROTECT)
    characterDD = models.CharField(max_length=20,verbose_name='421主角上手白金',null=True)
    occurrenceDate = models.DateTimeField(verbose_name='資料發生日期')
    lastModify = models.DateTimeField(verbose_name='資料修改日期')
    visible = models.BooleanField(verbose_name='是否可見')
    needWaterMark = models.BooleanField(verbose_name='是否需要浮水印')
    point = models.IntegerField(verbose_name='耗費點數')
    permissionsLevel = models.IntegerField(verbose_name='權限等級')
    DBClass = models.ForeignKey("DBClassInfo",verbose_name='資料庫類別',on_delete=models.PROTECT)
#資料庫類別對應表
class DBClassInfo(models.Model):

    DBClassName = models.CharField(max_length=100,verbose_name='名稱')
    DBClassCode = models.CharField(max_length=50,verbose_name='編碼')


#主類別對應表
class mainClassInfo(models.Model):

    mainClassName = models.CharField(max_length=50,verbose_name='主類別名稱',null=True)

#次類別對應表
class secClassInfo(models.Model):
    secClassName = models.CharField(max_length=50, verbose_name='主類別名稱', null=True)

#檔案類型對應表
class fileTypeInfo(models.Model):

    fileTypeName = models.CharField(max_length=50,verbose_name='檔案類型對應表',null=True)

#資料來源對應表
class sourceFromInfo(models.Model):
    sourceFromName = models.CharField(max_length=50, verbose_name='資料來源名稱', null=True)

class fileDataKeywords(models.Model):
    fileDataInfoID = models.ForeignKey('fileDataInfo',verbose_name='對應的資料ID',on_delete=models.CASCADE)
    keyword = models.CharField(max_length=20, verbose_name='關鍵字名稱', null=True)

#個人持有資料
class personalFileData(models.Model):
    fileDataID = models.ForeignKey('fileDataInfo',on_delete=models.CASCADE,verbose_name='對應的資料ID')
    ownerAccount = models.ForeignKey('userlogin.UserAccountInfo',on_delete=models.CASCADE,verbose_name='對應的帳號')
    exchangeDate = models.DateField(verbose_name='資料兌換日期',default=timezone.now)
    expiryDate = models.DateField(verbose_name='資料兌換時效到期日',null=True)
    costPoint = models.IntegerField(verbose_name='花費點數')
    waterCreateReady = models.BooleanField(default=0,verbose_name='浮水印是否完成')
    waterMarkPath = models.CharField(max_length=200,verbose_name='浮水印檔案路徑', null=True)

class personalExchangeFileLog(models.Model):
    fileDataID = models.ForeignKey('fileDataInfo', on_delete=models.CASCADE, verbose_name='對應的資料ID')
    ownerAccount = models.ForeignKey('userlogin.UserAccountInfo', on_delete=models.CASCADE, verbose_name='對應的帳號')
    exchangeDate = models.DateField(verbose_name='資料兌換日期',default=timezone.now)
    costPoint = models.IntegerField(verbose_name='花費點數')

#建立主類別表內容
# from NutriliteSearchPage.models import mainClassInfo
# inputDataList = ["營養","美容","科技","金鍋","其他","總部會議/活動","演講廳"]
# for data in inputDataList:
#     r = mainClassInfo.objects.create(mainClassName=data)
#     r.save()
#
# #建立次類別表內容
# from NutriliteSearchPage.models import secClassInfo
# inputDataList = ["其他","基礎營養","曲線管理","機能性營養","疾病","紐崔萊農場",
#                  "基礎保養","整體造型","醫美相關","迷思破解",
#                  "空氣清淨機","淨水器",
#                  "金鍋","不沾鍋","食譜","AmwayHome","G&H","Satinique","Glister","XS系列",
#                  "教室課程","基礎會議","菁英會議","老師有約","每月之星",
#                  "成功領導人","公司創辦人","名人講堂","公司介紹","培訓資料"
#                  ]
# for data in inputDataList:
#     r = secClassInfo.objects.create(secClassName=data)
#     r.save()
#
# #建立資料來源表內容
# from NutriliteSearchPage.models import sourceFromInfo
# inputDataList = ["個人製作","教室製作","總部製作","行動大學","YouTube","公司資料","其他"]
# for data in inputDataList:
#     r = sourceFromInfo.objects.create(sourceFromName=data)
#     r.save()

#建立檔案類型對應表內容
# from NutriliteSearchPage.models import fileTypeInfo
# inputDataList = ["影音檔","PDF","PPT","WORD","圖片/照片","純文字檔","其他"]
# for data in inputDataList:
#     r = fileTypeInfo.objects.create(fileTypeName=data)
#     r.save()
#假資料測試
# from NutriliteSearchPage.models import fileDataInfo,fileDataKeywords,mainClassInfo,secClassInfo,sourceFromInfo,fileTypeInfo,DBClassInfo
# r = fileDataInfo(
#     mainClass = mainClassInfo.objects.get(id=1),
#     secClass = secClassInfo.objects.get(id=2),
#     describe = "測試資料這是描述",
#     PDF = "1Cvx9Nfp7M-YP9jXp1gVmSPBmeBplX08b",
#     file = "15cweTBeTFKbXFft-vAe5_6r849FRAUxM",
#     fileType = fileTypeInfo.objects.get(id=5),
#     sourceForm = sourceFromInfo.objects.get(id=2),
#     sourceURL = None,
#     sourceScreenshot = None,
#     characterName = None,
#     characterClass = None,
#     characterDD = None,
#     occurrenceDate = "2021-08-01 00:00:00",
#     lastModify = "2021-08-16 00:00:00",
#     visible = 1,
#     permissionsLevel = 0)
# r.save()
#
# k = fileDataKeywords(
#     fileDataInfoID = r,
#     keyword = "關鍵字A",
# )
# k.save()
# k = fileDataKeywords(
#     fileDataInfoID = r,
#     keyword = "keywordB",
# )
# k.save()

# r = fileDataInfo(
#     mainClass = mainClassInfo.objects.get(id=1),
#     secClass = secClassInfo.objects.get(id=3),
#     describe = "測試資料這是描述2",
#     PDF = "1n7BL2UJUQkEXR6h4fWORQ9ZoboqR2TCl",
#     file = "1leqOZSLAgRpN55ulnUBAZWNr5nZsthE_",
#     fileType = fileTypeInfo.objects.get(id=5),
#     sourceForm = sourceFromInfo.objects.get(id=2),
#     sourceURL = None,
#     sourceScreenshot = None,
#     characterName = None,
#     characterClass = None,
#     characterDD = None,
#     occurrenceDate = "2021-08-01 00:00:00",
#     lastModify = "2021-08-16 00:00:00",
#     visible = 1,
#     permissionsLevel = 0)
# r.save()
#
# k = fileDataKeywords(
#     fileDataInfoID = r,
#     keyword = "關鍵字A2",
# )
# k.save()
# k = fileDataKeywords(
#     fileDataInfoID = r,
#     keyword = "keywordB2",
# )
# k.save()
#影片
# r = fileDataInfo(
#     mainClass = mainClassInfo.objects.get(id=1),
#     secClass = secClassInfo.objects.get(id=4),
#     describe = "對抗3C藍光威脅，紐崔萊晶明錠可為你層層守護",
#     PDF = "1n7Y_L9Nj4IpfJYj5WVWU59xVtYJK7abN",
#     file = "1n7Y_L9Nj4IpfJYj5WVWU59xVtYJK7abN",
#     fileType = fileTypeInfo.objects.get(id=1),
#     sourceForm = sourceFromInfo.objects.get(id=5),
#     sourceURL = "https://www.youtube.com/watch?v=wM4vUJ7mr7g",
#     sourceScreenshot = "https://drive.google.com/open?id=1PAvoqZ5d-iuoct62bMSBRtCHZJjrKszC",
#     characterName = None,
#     characterClass = None,
#     characterDD = None,
#     occurrenceDate = "2021-08-01 00:00:00",
#     lastModify = "2021-08-21 00:00:00",
#     visible = 1,
#     permissionsLevel = 0,
#     point=5,
#     DBClass=DBClassInfo.objects.get(id=2))
# r.save()
#
# keywordList = ["眼睛","晶明錠","3C","藍光","金盞花","歐越莓","黑醋栗","菠菜","葉黃素","花青素","類胡蘿蔔素"]
# for i in keywordList:
#     k = fileDataKeywords(
#         fileDataInfoID = r,
#         keyword =  i,
#     )
#     k.save()
