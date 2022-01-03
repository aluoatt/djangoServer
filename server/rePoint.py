from pointManage.models import pointHistory
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, UserAccountAmwayInfo, chainYenJobTitleInfo
from django.db.models import F, Value
import datetime

userChainyenList = UserAccountChainYenInfo.objects.all()
for chainyener in userChainyenList:
    if chainyener.UserAccountInfo.username in ["30036946029", "00000000000"]:
        continue
    reducePoint = chainyener.point
    chainyener.point = 50
    chainyener.save()
    modifier = UserAccountInfo.objects.get(username="00000000000")
    pHistory = pointHistory(UserAccountInfo = chainyener.UserAccountInfo, modifier = modifier.user,
                            recordDate = str(datetime.datetime.now()), reason = '月初點數重置',
                            addPoint = reducePoint, reducePoint = "", transferPoint = "",
                            resultPoint = 0)
    #pHistory.save()
    if chainyener.UserAccountInfo.username in ["73431717655", "30036948963", "30036946029", "00000000000"]:
        continue
    userAmwayAward =  UserAccountAmwayInfo.objects.get(UserAccountInfo = chainyener.UserAccountInfo)
    if userAmwayAward.amwayAward.rank >= 50:
        continue
    pHistory = pointHistory(UserAccountInfo = chainyener.UserAccountInfo, modifier = modifier.user,
                            recordDate = str(datetime.datetime.now()), reason = '月初點數給予',
                            addPoint = "50", reducePoint = "", transferPoint = "",
                            resultPoint = 50)
    #pHistory.save()

amwayAwardList = UserAccountAmwayInfo.objects.filter(amwayAward__rank__range=(50, 55))
for userAward in amwayAwardList:
    userAccount = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAward.UserAccountInfo)
    userAccount.point = 250
    userAccount.save()
    modifier = UserAccountInfo.objects.get(username="00000000000")
    pHistory = pointHistory(UserAccountInfo = chainyener.UserAccountInfo, modifier = modifier.user,
                            recordDate = str(datetime.datetime.now()), reason = "月初點數給予",
                            addPoint = "250", reducePoint = "", transferPoint = "",
                            resultPoint = 250)
    pHistory.save()

amwayAwardList = UserAccountAmwayInfo.objects.filter(amwayAward__rank__range=(60, 95))
for userAward in amwayAwardList:
    if userAward.UserAccountInfo.username in ["73431717655", "30036948963", "30036946029", "00000000000"]:
        continue
    userAccount = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAward.UserAccountInfo)
    userAccount.point = 300
    userAccount.save()
    modifier = UserAccountInfo.objects.get(username="00000000000")
    pHistory = pointHistory(UserAccountInfo = userAward.UserAccountInfo, modifier = modifier.user,
                            recordDate = str(datetime.datetime.now()), reason = "月初點數給予",
                            addPoint = "300", reducePoint = "", transferPoint = "",
                            resultPoint = 300)
    pHistory.save()

userAccount = UserAccountInfo.objects.get(username="73431717655")
userChainyen = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAccount)
userChainyen.point = 1000
userChainyen.save()
modifier = UserAccountInfo.objects.get(username="00000000000")
pHistory = pointHistory(UserAccountInfo = userAccount, modifier = modifier.user,
                        recordDate = str(datetime.datetime.now()), reason = "月初點數給予",
                        addPoint = "1000", reducePoint = "", transferPoint = "",
                        resultPoint = 1000)
pHistory.save()

userAccount = UserAccountInfo.objects.get(username="30036948963")
userChainyen = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAccount)
userChainyen.point = 400
userChainyen.save()
modifier = UserAccountInfo.objects.get(username="00000000000")
pHistory = pointHistory(UserAccountInfo = userAccount, modifier = modifier.user,
                        recordDate = str(datetime.datetime.now()), reason = "月初點數給予",
                        addPoint = "400", reducePoint = "", transferPoint = "",
                        resultPoint = 400)
pHistory.save()

