from django.contrib.auth.hashers import make_password
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, chainYenJobTitleInfo, chainYenClassInfo,UserAccountAmwayInfo, registerDDandDimInfo, amwayAwardInfo
from userlogin.models import TempUserAccountInfo, TempUserAccountAmwayInfo, TempUserAccountChainYenInfo
import random
def createUser(amwayNumber, amAward, ddInfo, user, username, jobTitle, classInfo):
    r = UserAccountInfo(username = username,
        user=user,
        gender="男",
        phone="000000000",
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
        point=10000,
        EM=False)

    r3 = UserAccountAmwayInfo(UserAccountInfo=r,
        amwayNumber=amwayNumber,
        amwayAward=amAward,
        amwayDD=ddInfo)
    r.save()
    r2.save()
    r3.save()

# 指定給白金
DDNumber = "2000000"
Diamond  = "1000000"
for i in range(3):
    user = "我的 DD 是白金" + str(i)
    amwayNumber = str(3000000 + i)
    IDNumber = str(3000 + i)
    username = amwayNumber + IDNumber
    jobTitle = chainYenJobTitleInfo.objects.get(jobTitle = "無")
    classInfo = chainYenClassInfo.objects.get(ClassRoomName = "台北")
    amAward = amwayAwardInfo.objects.get(amwayAward = "直銷商")
    ddInfo = registerDDandDimInfo.objects.get(amwayNumber = DDNumber)

    createUser(amwayNumber, amAward, ddInfo, user, username, jobTitle, classInfo)

