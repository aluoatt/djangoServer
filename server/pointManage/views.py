from django.shortcuts import render
from userlogin.models import UserAccountInfo
from django.contrib.auth.decorators import permission_required
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo
from django.db.models import F, Value
from django.http import HttpResponse
from pointManage.models import pointHistory
from django.core import serializers
import datetime
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
        pHistory = pointHistory.objects.filter(UserAccountInfo = userAccountInfo)
        res.status_code = 200
        res.content =  serializers.serialize("json", pHistory)
    except:
        res.status_code = 503

    return res
