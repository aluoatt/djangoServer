from django.contrib.auth.hashers import make_password
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, chainYenJobTitleInfo, chainYenClassInfo,UserAccountAmwayInfo, registerDDandDimInfo, amwayAwardInfo
from userlogin.models import TempUserAccountInfo, TempUserAccountAmwayInfo, TempUserAccountChainYenInfo

from NutriliteSearchPage.models import sourceFromInfo


amAward = amwayAwardInfo.objects.get(amwayAward = "鑽石")

# 將測試使用者註冊註冊新的白金編號
ddInfo = registerDDandDimInfo.objects.filter(amwayNumber = "2000000")
if not ddInfo:
    ddInfo = registerDDandDimInfo(amwayAward=amAward, amwayNumber="2000000", amwayDiamond="1000000", main = "我是白金")
    ddInfo.save()
else:
    ddInfo = ddInfo.first()

#將自己的上手領導人設定為我是鑽石
ddInfo = registerDDandDimInfo.objects.get(amwayNumber = "1000000")

username = "20000002000"
classInfo = chainYenClassInfo.objects.get(ClassRoomName = "台北")
amAward = amwayAwardInfo.objects.get(amwayAward = "白金")
jobTitle = chainYenJobTitleInfo.objects.get(jobTitle = "無")

r = UserAccountInfo(username = username,
    user="我是白金",
    gender="男",
    phone="123456",
    password=make_password("a"),
    is_superuser=0,
    is_staff=1,
    is_active=1,
    dataPermissionsLevel=99,
    email="123@gmail.com")
r2 = UserAccountChainYenInfo(UserAccountInfo=r,
    jobTitle=jobTitle,
    classRoom=classInfo,
    accountStatus="正常",
    freezeDate=None,
    point=100000,
    EM=False)

r3 = UserAccountAmwayInfo(UserAccountInfo=r,
    amwayNumber="2000000",
    amwayAward=amAward,
    amwayDD=ddInfo)
r.save()
r2.save()
r3.save()
