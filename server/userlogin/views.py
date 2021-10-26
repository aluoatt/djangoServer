import json

from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from userlogin.models import amwayAwardInfo ,chainYenJobTitleInfo ,chainYenClassInfo , UserAccountInfo,UserAccountChainYenInfo
from userlogin.models import TempUserAccountInfo ,TempUserAccountAmwayInfo ,\
    TempUserAccountChainYenInfo,registerDDandDimInfo,loginHistory,ConfirmStringForPWD
from pointManage.models import pointHistory
from django.contrib.auth.hashers import make_password
import datetime
from django.contrib.sessions.models import Session
key = "Ja8asdfnjQnasdfd72D"

# def set_session_key(self, key):
#     if self.last_session_key and not self.last_session_key == key:
#         Session.objects.get(session_key=self.last_session_key).delete()
#     self.last_session_key = key
#     self.save()
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    username = request.POST.get('username', '')
    idnumber = request.POST.get('idnumber', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username + idnumber, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        # UserAccountInfo.set_session_key(request.session.session_key)
        user.set_session_key(request.session.session_key)
        userAccountInfo = UserAccountInfo.objects.get(username=request.user)
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=userAccountInfo.id)
        if UserAccountChainYen.point - 1 <= 0:
            auth.logout(request)
            return redirect('/accounts/login/?pointNotEnought=False')
        UserAccountChainYen.point -= 1
        UserAccountChainYen.save()
        pHistory = pointHistory(UserAccountInfo=userAccountInfo, modifier="系統",
                                recordDate=datetime.datetime.now(), reason='登入扣點',
                                addPoint="", reducePoint="1", transferPoint="",
                                resultPoint=UserAccountChainYen.point)
        pHistory.save()
        try:
            loginHistory.objects.create(user=request.user, ip=request.META['HTTP_X_FORWARDED_FOR'])
        except :
            pass
        return HttpResponseRedirect('/home/')
    else:
        if username != '':
            return redirect('/accounts/login/?pwderror=False')
        return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# @permission_required('userlogin.can_see_register', login_url='/accounts/userlogin/')
def register(request,token):
    # try:
        user = None
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
    token = generate_token(key, 7200)

    # return redirect('/accounts/register/' + token)
    return HttpResponse(json.dumps({"result":settings.MYIP+'/accounts/register/' + token}), content_type="application/json")
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

def forgetPasswordKeyinNumber(request):
    return render(request, 'forgetPWD/forgetPWDpage.html', locals())

def forgetPasswordGetMail(request):
    r'''
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''

    try:
        amwayId = request.POST.get("amwayId")
        lastNumber = request.POST.get("lastNumber")
        UserAccount= UserAccountInfo.objects.get(username=amwayId+lastNumber)
        code = make_confirm_string(UserAccount.username)
        send_email(UserAccount.email, code)
        message = "信件送出成功，請至註冊的email中收信"

    except:
        message="編號不存在，請洽管理員"

    return render(request, 'personalInfoPages/changePasswordOptionResult.html', locals())

def forgetPasswordModify(request):
    r'''
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''
    code = request.POST.get('code', None)
    id_password1 = request.POST.get("id_password1")
    id_password2 = request.POST.get("id_password2")

    message = ''
    try:
        confirm = ConfirmStringForPWD.objects.get(code=code)
    except:
        message = '無效的確認請求!'
        return render(request, 'personalInfoPages/changePasswordOptionResult.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.PWD_CONFIRM_MIN):
        confirm.delete()
        message = '您的郵件已經過期，請再試一次!'
        return render(request, 'personalInfoPages/changePasswordOptionResult.html', locals())
    else:

        if id_password1 == id_password2:
            r = UserAccountInfo.objects.get(username=confirm.user_name)
            r.password = make_password(id_password1)
            r.save()
            message = "修改成功，請重新登入"
        else:
            message = "修改失敗，請再試一次"

        confirm.delete()

        return render(request, 'personalInfoPages/changePasswordOptionResult.html', locals())


def forgetPasswordConfirmPage(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmStringForPWD.objects.get(code=code)
    except:
        message = '無效的確認請求!'
        return render(request, 'personalInfoPages/changePasswordOptionResult.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.PWD_CONFIRM_MIN):
        confirm.delete()
        message = '您的郵件已經過期，請再試一次!'
        return render(request, 'managerPages/userAccountConfirm.html', locals())
    else:
        # confirm.delete()
        return render(request, 'forgetPWD/forgetPWDModifypage.html', locals())
    
    

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '來自群雁資訊檢索系統的密碼修改確認信'

    text_content = '''
                    *此信件為系統發出信件，請勿直接回覆，感謝您的配合，謝謝!*
                    感謝您註冊自群雁資訊檢索系統！
                    如果你看到這則消息，說明你的信箱不提供HTML連接功能，請洽會長或上手白金！'''

    html_content = '''
                    <p>*此信件為系統發出信件，請勿直接回覆，感謝您的配合，謝謝!*<p>
                    <p>請點連結修改密碼</p>                  
                    
                    <p><a href="{}/accounts/forgetPassword/confirmPage?code={}" target=blank>確認連結</a></p>
                    <p>此連結的有效期為{}分鐘！</p>
                    '''.format(settings.MYIP, code, settings.PWD_CONFIRM_MIN)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

import hashlib

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user, now)
    ConfirmStringObj = ConfirmStringForPWD.objects.filter(user_name=user)
    if ConfirmStringObj.count() > 0 :
        ConfirmStringObj.first().delete()

    ConfirmStringForPWD.objects.create(code=code, user_name=user)
    return code