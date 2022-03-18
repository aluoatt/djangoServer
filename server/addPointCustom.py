from pointManage.models import pointHistory
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, UserAccountAmwayInfo, chainYenJobTitleInfo
import datetime

userChainyenList = UserAccountChainYenInfo.objects.all()
for chainyener in userChainyenList:
    addPoint = 50 - chainyener.point
    chainyener.point = 50
    chainyener.save()
    modifier = UserAccountInfo.objects.get(username="00000000000")
    #modifier = UserAccountInfo.objects.get(username="10000001000")
    pHistory = pointHistory(UserAccountInfo = chainyener.UserAccountInfo, modifier = modifier.user,
                            recordDate = str(datetime.datetime.now()), reason = '善用點數獎勵加點',
                            addPoint = addPoint, reducePoint = "", transferPoint = "",
                            resultPoint = 50)
    pHistory.save()
