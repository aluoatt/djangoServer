from django.shortcuts import render
from userlogin.models import UserAccountInfo, amwayAwardInfo, registerDDandDimInfo
from django.contrib.auth.decorators import permission_required
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, UserAccountAmwayInfo, chainYenJobTitleInfo
from django.db.models import F, Value
from django.http import HttpResponse
from pointManage.models import pointHistory
from django.core import serializers
import datetime, json
# Create your views here.

@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def addPoint(request):
    res = HttpResponse()
    try:
        userAccountInfo = UserAccountInfo.objects.get(username = request.POST['username'])
        accountChainyen = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAccountInfo)
        point = accountChainyen.point + 10
        accountChainyen.point = F('point') + 10
        accountChainyen.save()

        res.status_code = 200
        res.content = point

        modifier = request.user.user
        pHistory = pointHistory(UserAccountInfo = userAccountInfo, modifier = modifier,
                                recordDate = datetime.datetime.now(), reason = '管理者加點',
                                addPoint = "+10", reducePoint = "", transferPoint = "",
                                resultPoint = point)
        pHistory.save()
    except:
        res.status_code = 503

    return res

@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def addPointByAll(request):
    res = HttpResponse()
    try:
        point = 0
        try:
            point = int(request.POST["point"])
        except:
            point = 0
        if point == 0:
            res.status_code = 200
            return res

        userAccountChainyenList = UserAccountChainYenInfo.objects.all()
        userAccountChainyenList.update(point=F('point') + point)

        res.status_code = 200

        modifier = request.user.user
        for userAccountChainyen in userAccountChainyenList:
            userAccount = userAccountChainyen.UserAccountInfo
            resultPoint = userAccountChainyen.point
            pHistory = pointHistory(UserAccountInfo = userAccount, modifier = modifier,
                                    recordDate = datetime.datetime.now(), reason = '管理者加點',
                                    addPoint = "+" + str(point), reducePoint = "", transferPoint = "",
                                    resultPoint = resultPoint)
            pHistory.save()

    except:
        res.status_code = 404

    return res


@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def addPointByAmwayAward(request):
    res = HttpResponse()
    try:
        amwayAward = ""
        if "amwayAward" in request.POST:
            amwayAward = request.POST['amwayAward']
        if amwayAward:
            try:
                amwayAward = amwayAwardInfo.objects.get(amwayAward=amwayAward)
            except:
                amwayAward = ""
        point = 0
        try:
            point = int(request.POST["point"])
        except:
            point = 0
        if point == 0:
            res.status_code = 200
            return res

        if amwayAward:
            accountIDList = UserAccountAmwayInfo.objects.filter(amwayAward = amwayAward).values('UserAccountInfo')
            accountInfoList = UserAccountInfo.objects.filter(id__in=accountIDList).exclude(username = request.user.username)
            userAccountChainyenList = UserAccountChainYenInfo.objects.filter(UserAccountInfo__in=accountInfoList)
            userAccountChainyenList.update(point=F('point') + point)
        else:
            res.status_code = 404
            return res

        res.status_code = 200

        modifier = request.user.user
        for userAccountChainyen in userAccountChainyenList:
            userAccount = userAccountChainyen.UserAccountInfo
            resultPoint = userAccountChainyen.point
            pHistory = pointHistory(UserAccountInfo = userAccount, modifier = modifier,
                                    recordDate = datetime.datetime.now(), reason = '管理者加點',
                                    addPoint = "+" + str(point), reducePoint = "", transferPoint = "",
                                    resultPoint = resultPoint)
            pHistory.save()

    except:
        res.status_code = 404

    return res

@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def addPointByJobTitle(request):
    res = HttpResponse()
    try:
        jobTitle = ""
        if "jobTitle" in request.POST:
            jobTitle = request.POST['jobTitle']
        if jobTitle:
            try:
                jobTitle = chainYenJobTitleInfo.objects.get(jobTitle = jobTitle)
            except:
                jobTitle = ""
        
        point = 0
        try:
            point = int(request.POST["point"])
        except:
            point = 0
        if point == 0:
            res.status_code = 200
            return res

        if jobTitle:
            userAccountChainyenList = UserAccountChainYenInfo.objects.filter(jobTitle=jobTitle)
            userAccountChainyenList.update(point=F('point') + point)
        else:
            res.status_code = 404
            return res

        res.status_code = 200

        modifier = request.user.user
        for userAccountChainyen in userAccountChainyenList:
            userAccount = userAccountChainyen.UserAccountInfo
            resultPoint = userAccountChainyen.point
            pHistory = pointHistory(UserAccountInfo = userAccount, modifier = modifier,
                                    recordDate = datetime.datetime.now(), reason = '管理者加點',
                                    addPoint = "+" + str(point), reducePoint = "", transferPoint = "",
                                    resultPoint = resultPoint)
            pHistory.save()

    except:
        res.status_code = 503

    return res


@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def reducePoint(request):
    res = HttpResponse()
    try:
        userAccountInfo = UserAccountInfo.objects.get(username = request.POST['username'])
        accountChainyen = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAccountInfo)
        point = accountChainyen.point -1
        accountChainyen.point = F('point') - 1
        accountChainyen.save()

        res.status_code = 200
        res.content = point

        modifier = request.user.user
        pHistory = pointHistory(UserAccountInfo = userAccountInfo, modifier = modifier,
                                recordDate = datetime.datetime.now(), reason = '管理者扣點',
                                addPoint = "", reducePoint = "-1", transferPoint = "",
                                resultPoint = point)
        pHistory.save()
    except:
        res.status_code = 503

    return res



@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def getPointHistory(request):
    res = HttpResponse()
    try:
        userAccountInfo = UserAccountInfo.objects.get(username = request.POST['username'])
        pHistory = pointHistory.objects.filter(UserAccountInfo = userAccountInfo).order_by('-recordDate')
        res.status_code = 200
        res.content =  serializers.serialize("json", pHistory)
    except:
        res.status_code = 503

    return res


def transferPoint(request):
    res = HttpResponse()
    try:

        fromUser = request.user.username
        toUser = request.POST['username']
        pointTransfer = int(request.POST['point'])

        #Do not hack me
        if pointTransfer <= 0:
            res.status_code = 404
            res.content = "do not try to hack me <3"
            return res

        #TODO restrict the transfer outside self Team when someone hack this API
        fromUserAccount = UserAccountInfo.objects.get(username = fromUser)
        fromUserAmwayAccount = UserAccountAmwayInfo.objects.get(UserAccountInfo = fromUserAccount)
        fromUserAmwayNumber = fromUserAmwayAccount.amwayNumber
        toUserAccount = UserAccountInfo.objects.get(username = toUser)
        toUserAmwayAccountInfo = UserAccountAmwayInfo.objects.get(UserAccountInfo=toUserAccount)
        toUserDDInfo = toUserAmwayAccountInfo.amwayDD

        #Do not hack me
        if not (toUserDDInfo.amwayNumber  == fromUserAmwayNumber or 
                int(toUserDDInfo.amwayDiamond) == fromUserAmwayNumber):
            res.status_code = 404
            res.content = "do not try to hack me <3"
            return res
        
        #扣點
        userAccountInfo = UserAccountInfo.objects.get(username = fromUser)
        accountChainyen = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAccountInfo)
        fromResultPoint = accountChainyen.point - pointTransfer
        if fromResultPoint < 0:
            res.status_code = 404
            res.content = "point not enough"
            return res
        accountChainyen.point = F('point') - pointTransfer
        accountChainyen.save()

        modifier = request.user.user
        pHistory = pointHistory(UserAccountInfo = userAccountInfo, modifier = modifier,
                                recordDate = datetime.datetime.now(), reason = '轉讓點數',
                                addPoint = "", reducePoint = "", transferPoint = "-" + str(pointTransfer),
                                resultPoint = fromResultPoint)
        pHistory.save()

        #加點
        userAccountInfo = UserAccountInfo.objects.get(username = toUser)
        accountChainyen = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAccountInfo)
        toResultPoint = accountChainyen.point + int(pointTransfer)
        accountChainyen.point = F('point') + int(pointTransfer)
        accountChainyen.save()

        res.status_code = 200
        res.content = json.dumps({
            "fromUser": fromUser,
            "toUser": toUser,
            "fromResultPoint": fromResultPoint,
            "toResultPoint": toResultPoint
        })

        modifier = request.user.user
        pHistory = pointHistory(UserAccountInfo = userAccountInfo, modifier = modifier,
                                recordDate = datetime.datetime.now(), reason = '轉讓點數',
                                addPoint = "", reducePoint = "", transferPoint = "+" + str(pointTransfer),
                                resultPoint = toResultPoint)
        pHistory.save()
    except:
        res.status_code = 503

    return res
