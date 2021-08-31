from django.shortcuts import render
from userlogin.models import UserAccountInfo
from django.contrib.auth.decorators import permission_required
from userlogin.models import UserAccountInfo, UserAccountChainYenInfo
from django.db.models import F, Value
from django.http import HttpResponse
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
    except:
        res.status_code = 503

    return res


@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def pointHistory(request):
    res = HttpResponse()
    try:
        userAccountInfo = UserAccountInfo.objects.get(username = request.POST['username'])
        accountChainyen = UserAccountChainYenInfo.objects.get(UserAccountInfo = userAccountInfo)
        res.status_code = 200
    except:
        res.status_code = 503

    return res
