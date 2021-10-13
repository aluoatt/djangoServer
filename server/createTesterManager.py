from django.contrib.auth.hashers import make_password
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, chainYenJobTitleInfo, chainYenClassInfo,UserAccountAmwayInfo, registerDDandDimInfo, amwayAwardInfo
from userlogin.models import TempUserAccountInfo, TempUserAccountAmwayInfo, TempUserAccountChainYenInfo
import random
from django.contrib.auth.models import Permission
def createManager(amwayNumber, amAward, ddInfo, user, username, jobTitle, classInfo):
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

    # Assign permission
    userAccount = UserAccountInfo.objects.get(username = username)
    perm = Permission.objects.get(codename="seeManagerMenuButton")
    userAccount.user_permissions.add(perm)
    perm = Permission.objects.get(codename="seeManagerPointPage")
    userAccount.user_permissions.add(perm)
    perm = Permission.objects.get(codename="seeManagerAccountManagerPage")
    userAccount.user_permissions.add(perm)

preAmwayNumber = "100000"
preDiamond     = "100000"
preMain        = ""
for i in range(4):
    user = "直銷商" + str(i)
    amwayNumber = str(8000000 + i)
    IDNumber = str(8000 + i)
    username = amwayNumber + IDNumber
    jobTitle = chainYenJobTitleInfo.objects.get(jobTitle = "無")
    classInfo = chainYenClassInfo.objects.get(ClassRoomName = "台北")
    amAward = amwayAwardInfo.objects.get(amwayAward = "白金")

    ddInfo = registerDDandDimInfo.objects.filter(amwayNumber = preAmwayNumber)
    if not ddInfo:
        ddInfo = registerDDandDimInfo(amwayAward=amAward, amwayNumber=preAmwayNumber,
                                      amwayDiamond=preMain, main = preMain)
        ddInfo.save()
    else:
        ddInfo = ddInfo.get()

    createManager(amwayNumber, amAward, ddInfo, user, username, jobTitle, classInfo)

