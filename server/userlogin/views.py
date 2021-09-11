import json

from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from userlogin.models import amwayAwardInfo ,chainYenJobTitleInfo ,chainYenClassInfo , UserAccountInfo,UserAccountChainYenInfo
from userlogin.models import TempUserAccountInfo ,TempUserAccountAmwayInfo ,TempUserAccountChainYenInfo,registerDDandDimInfo
from pointManage.models import pointHistory
from django.contrib.auth.hashers import make_password
import datetime
import logging

key = "Ja8asdfnjQnasdfd72D"

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    username = request.POST.get('username', '')
    idnumber = request.POST.get('idnumber', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username + idnumber, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        userAccountInfo = UserAccountInfo.objects.get(username=request.user)
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=userAccountInfo.id)
        if UserAccountChainYen.point - 1 <= 0:
            auth.logout(request)
            pwderror = False
            pointNotEnought = True
            return render(request, 'login.html', locals())
        UserAccountChainYen.point -= 1
        UserAccountChainYen.save()
        pHistory = pointHistory(UserAccountInfo=userAccountInfo, modifier="系統",
                                recordDate=datetime.datetime.now(), reason='登入扣點',
                                addPoint="", reducePoint="1", transferPoint="",
                                resultPoint=UserAccountChainYen.point)
        pHistory.save()
        return HttpResponseRedirect('/home/')
    else:
        if username != '':

            pwderror = True
        return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# @permission_required('userlogin.can_see_register', login_url='/accounts/userlogin/')
def register(request,token):
    # try:
        if certify_token(key, token):
            accountName = ''
            username = ''
            IDnumber = ''
            gander = ''
            phone = ''
            chainYenJobTitle = ''
            amwayAward = ''
            ChainYenClass = ''
            babysitter = ''
            amwayDD = ''
            amwayDiamond = ''
            id_password1 = ''
            id_password2 = ''
            EM = ''
            e_mail=''
            passwordConfirm = False
            regSuccess = False
            if request.method == 'POST':
                form = UserCreationForm()
                accountName = request.POST.get('accountName', '')
                username = request.POST.get('username', '')
                IDnumber = request.POST.get('IDnumber', '')
                gander = request.POST.get('gander', '')
                phone = request.POST.get('phone', '')
                chainYenJobTitle = request.POST.get('chainYenJobTitle', '')
                amwayAward = request.POST.get('amwayAward','')
                ChainYenClass = request.POST.get('ChainYenClass','')
                babysitter = request.POST.get('babysitter', '')
                amwayDD = request.POST.get('amwayDD', '')
                amwayDiamond = request.POST.get('amwayDiamond', '')
                id_password1 = request.POST.get('password1', '')
                id_password2 = request.POST.get('password2', '')
                EM = request.POST.get('EM', '')
                e_mail = request.POST.get('e_mail', '')

                if EM == "True":
                    EM = True
                else:
                    EM = False

                amwayawards = amwayAwardInfo.objects.all()
                ChainYenJobTitles = chainYenJobTitleInfo.objects.all()
                ChainYenClassInfos = chainYenClassInfo.objects.all()

                if id_password1 != id_password2:

                    passwordConfirm = True
                    return render(request, 'register.html', locals())
                if (TempUserAccountInfo.objects.filter(username=accountName + IDnumber).count() > 0
                        or UserAccountInfo.objects.filter(username=accountName + IDnumber).count() > 0):
                    return redirect('/accounts/registerSuccessStatus/exist')
                else:
                    r = TempUserAccountInfo(username = accountName+IDnumber,
                                            user=username,
                                            gender = gander,
                                            phone = phone,
                                            password = make_password(id_password1),
                                            # is_superuser = 0,
                                            # is_staff =0,
                                            # is_active=1,
                                            auditStatus = "審核中",
                                            email=e_mail,
                                            dataPermissionsLevel=1)

                    r2 = TempUserAccountChainYenInfo(UserAccountInfo = r,
                                                 jobTitle = chainYenJobTitleInfo.objects.get(id=chainYenJobTitle),
                                                 classRoom = chainYenClassInfo.objects.get(id=ChainYenClass),

                                                 accountStatus="正常",
                                                 freezeDate=None,
                                                 point=0,
                                                 EM=EM)

                    r3 = TempUserAccountAmwayInfo(UserAccountInfo= r,
                                              amwayNumber=accountName,
                                              amwayAward=amwayAwardInfo.objects.get(id=amwayAward),
                                              amwayDD=registerDDandDimInfo.objects.get(amwayNumber = amwayDD))

                    r.save()
                    r2.save()
                    r3.save()

                    return redirect('/accounts/registerSuccessStatus/success')

            else:
                form = UserCreationForm()
                amwayawards = amwayAwardInfo.objects.all().order_by('rank')
                ChainYenJobTitles = chainYenJobTitleInfo.objects.all().order_by('rank')
                ChainYenClassInfos = chainYenClassInfo.objects.all().order_by('rank')
            return render(request, 'register.html', locals())
        else:
            return HttpResponseNotFound('<h1>註冊暫時不開放，如欲註冊請洽會長</h1>')
    # except:
    #     return HttpResponseNotFound('<h1>註冊暫時不開放，如欲註冊請洽會長</h1>')

def registerSuccess(request,status):
    return render(request, 'registerSuccessStatus.html', locals())


@permission_required('userlogin.can_see_register', login_url='/accounts/userlogin/')
def createRegisterPage(request):
    token = generate_token(key, 3600)

    return redirect('/accounts/register/' + token)

#找DD是否存在
def checkRegDD(request):
    response_data = {}
    try:
        DDNumber = int(json.loads(request.body.decode('utf-8'))["num"])
    except:
        DDNumber =0

    DDinfo_obj = registerDDandDimInfo.objects.filter(amwayNumber=DDNumber)
    if DDinfo_obj.count() < 1:
        response_data['status'] = False
        response_data['diamond'] = ''
    else:

        response_data['status'] = True
        if DDinfo_obj.first().sec==None :
            response_data['DDname'] = DDinfo_obj.first().main
        else:
            response_data['DDname'] = DDinfo_obj.first().main+"/" + DDinfo_obj.first().sec
        response_data['diamond'] = registerDDandDimInfo.objects.get(amwayNumber=DDinfo_obj.first().amwayDiamond).main
    return HttpResponse(json.dumps(response_data), content_type="application/json")

import time
import base64
import hmac

def generate_token(key, expire=3600):
    r'''
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

def certify_token(key, token):
    r'''
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True