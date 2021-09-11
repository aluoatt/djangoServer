from django.contrib.auth.hashers import make_password
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, chainYenJobTitleInfo, chainYenClassInfo,UserAccountAmwayInfo, registerDDandDimInfo, amwayAwardInfo
from userlogin.models import TempUserAccountInfo, TempUserAccountAmwayInfo, TempUserAccountChainYenInfo

from NutriliteSearchPage.models import sourceFromInfo


amAward = amwayAwardInfo.objects.get(amwayAward = "創辦人皇冠大使")
ddInfo = registerDDandDimInfo.objects.filter(amwayAward = amAward)
if not ddInfo:
    ddInfo = registerDDandDimInfo(amwayAward=amAward, amwayNumber="000000", amwayDiamond="administrator", main = "administrator")
    ddInfo.save()
else:
    ddInfo = ddInfo.get()

username = "administrator"
classInfo = chainYenClassInfo.objects.get(ClassRoomName = "台北")
amAward = amwayAwardInfo.objects.filter(amwayAward = "創辦人皇冠大使")
amAward = amAward.get()
jobTitle = chainYenJobTitleInfo.objects.filter(jobTitle = "超級管理者")
if(not jobTitle):
    jobTitle = chainYenJobTitleInfo(jobTitle = "超級管理者", rank=99)
    jobTitle.save()
else:
    jobTitle = jobTitle.get()
r = UserAccountInfo(username = username,
    user="超級使用者",
    gender="男",
    phone="123456",
    password=make_password("a"),
    is_superuser=1,
    is_staff=1,
    is_active=1,
    dataPermissionsLevel=99,
    email="123@gmail.com")
r2 = UserAccountChainYenInfo(UserAccountInfo=r,
    jobTitle=jobTitle,
    classRoom=classInfo,
    accountStatus="正常",
    freezeDate=None,
    point=0,
    EM=False)

r3 = UserAccountAmwayInfo(UserAccountInfo=r,
    amwayNumber="000000",
    amwayAward=amAward,
    amwayDD=ddInfo)
r.save()
r2.save()
r3.save()
