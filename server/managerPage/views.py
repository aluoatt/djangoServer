import json

from django.http import HttpResponse
from django.contrib.auth.models import Permission


# Create your views here.
from . import models
from django.shortcuts import render
from django.db.models import Q

from userlogin.models import UserAccountInfo, UserAccountChainYenInfo, chainYenJobTitleInfo
from userlogin.models import chainYenClassInfo, registerDDandDimInfo, amwayAwardInfo, ConfirmString,UserAccountAmwayInfo
from django.contrib.auth.decorators import permission_required
from userlogin.models import TempUserAccountInfo, TempUserAccountAmwayInfo, TempUserAccountChainYenInfo


# Create your views here.
import hashlib
import datetime
from django.conf import settings
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user, now)
    ConfirmStringObj = ConfirmString.objects.filter(user_name=user)
    if ConfirmStringObj.count() > 0 :
        ConfirmStringObj.first().delete()

    ConfirmString.objects.create(code=code, user_name=user)
    return code

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '來自群雁資訊檢索系統的確認信'

    text_content = '''感謝您註冊自群雁資訊檢索系統！\
                    如果你看到這則消息，說明你的信箱不提供HTML連接功能，請洽會長或上手白金！'''

    html_content = '''
                    <p>感謝您註冊自群雁資訊檢索系統</p>
                    <p>請點我認證註冊！</p>
                    <p><a href="{}/managerPages/userAccountConfirm?code={}" target=blank>確認連結</a></p>
                    <p>此連結的有效期為{}天！</p>
                    '''.format(settings.MYIP, code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def userAccountConfirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '無效的確認請求!'
        return render(request, 'managerPages/userAccountConfirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.delete()
        message = '您的郵件已經過期，請洽會長或上手白金!'
        return render(request, 'managerPages/userAccountConfirm.html', locals())
    else:
        tr = TempUserAccountInfo.objects.get(username=confirm.user_name)
        classChairMan = tr.tempuseraccountchainyeninfo_set.first().jobTitle.jobTitle == "會長"

        r = UserAccountInfo(username=tr.username,
                            user=tr.user,
                            gender=tr.gender,
                            phone=tr.phone,
                            password=tr.password,
                            is_superuser=0,
                            is_staff=0,
                            is_active=1,
                            dataPermissionsLevel=0,
                            email=tr.email)

        r2 = UserAccountChainYenInfo(UserAccountInfo=r,
                                     jobTitle=chainYenJobTitleInfo.objects.get(id=tr.tempuseraccountchainyeninfo_set.first().jobTitle.id),
                                     classRoom=chainYenClassInfo.objects.get(id=tr.tempuseraccountchainyeninfo_set.first().classRoom.id),
                                     accountStatus="正常",
                                     freezeDate=None,
                                     point=0,
                                     EM=tr.tempuseraccountchainyeninfo_set.first().EM)

        r3 = UserAccountAmwayInfo(UserAccountInfo=r,
                                  amwayNumber=tr.tempuseraccountamwayinfo_set.first().amwayNumber,
                                  amwayAward=amwayAwardInfo.objects.get(id=tr.tempuseraccountamwayinfo_set.first().amwayAward.id),
                                  amwayDD=registerDDandDimInfo.objects.get(amwayNumber=tr.tempuseraccountamwayinfo_set.first().amwayDD.amwayNumber)
                                  )

        r.save()
        r2.save()
        r3.save()

        if classChairMan:
            userAcconut = UserAccountInfo.objects.get(username=tr.username)
            perm = Permission.objects.get(codename=settings.CLASS_CHARIMAN_MANAGER_DICT[tr.tempuseraccountchainyeninfo_set.first().classRoom.ClassRoomName])
            userAcconut.user_permissions.add(perm)
            perm = Permission.objects.get(codename="can_see_register")
            userAcconut.user_permissions.add(perm)
            perm = Permission.objects.get(codename="seeManagerMenuButton")
            userAcconut.user_permissions.add(perm)
            perm = Permission.objects.get(codename="seeManagerAccountManagerPage")
            userAcconut.user_permissions.add(perm)
            perm = Permission.objects.get(codename="seeManagerAuditAccountPage")
            userAcconut.user_permissions.add(perm)
        tr.delete()
        confirm.delete()
        message = '恭喜您註冊成功!五秒後將自動跳轉到登入頁面。'
        return render(request, 'managerPages/userAccountConfirm.html', locals())

@permission_required('userlogin.seeManagerAccountManagerPage', login_url='/accounts/userlogin/')
def managerAccountManagerPage(request):
    tag = "ManagerAccountManagerPage"

    # 職務表
    jobTitles = chainYenJobTitleInfo.objects.all()
    # 獎銜表
    amwayAwards = amwayAwardInfo.objects.all().order_by('rank')
    # 教室表
    chainYenClasses = chainYenClassInfo.objects.all().order_by('rank')
    # 白金表
    registerDDs = registerDDandDimInfo.objects.filter(amwayAward__rank__gte=15)
    # 鑽石表
    registerDims = registerDDandDimInfo.objects.filter(amwayAward__rank__gte=60)

    q1 = Q()
    q1.connector = 'OR'
    q1.children.append(("classRoom__ClassRoomName", "無"))

    if request.user.has_perm('userlogin.CYPManager'):
        q1.children.append(("classRoom__ClassRoomName", "台北"))

    if request.user.has_perm('userlogin.CYLManager'):
        q1.children.append(("classRoom__ClassRoomName", "中壢"))

    if request.user.has_perm('userlogin.CYSManager'):
        q1.children.append(("classRoom__ClassRoomName", "新竹"))

    if request.user.has_perm('userlogin.CYZManager'):
        q1.children.append(("classRoom__ClassRoomName", "台中"))

    if request.user.has_perm('userlogin.CYJManager'):
        q1.children.append(("classRoom__ClassRoomName", "嘉義"))

    if request.user.has_perm('userlogin.CYN2Manager'):
        q1.children.append(("classRoom__ClassRoomName", "永康245"))

    if request.user.has_perm('userlogin.CYN1Manager'):
        q1.children.append(("classRoom__ClassRoomName", "永康135"))

    if request.user.has_perm('userlogin.CYMManager'):
        q1.children.append(("classRoom__ClassRoomName", "良美"))

    if request.user.has_perm('userlogin.CYKManager'):
        q1.children.append(("classRoom__ClassRoomName", "高雄"))

    if request.user.has_perm('userlogin.CYDManager'):
        q1.children.append(("classRoom__ClassRoomName", "屏東"))

    if request.user.has_perm('userlogin.CYWManager'):
        q1.children.append(("classRoom__ClassRoomName", "花蓮"))

    if request.user.has_perm('userlogin.CYTManager'):
        q1.children.append(("classRoom__ClassRoomName", "台東"))

    if request.user.has_perm('userlogin.CYHManager'):
        q1.children.append(("classRoom__ClassRoomName", "澎湖"))

    q2 = Q()
    q2.connector = 'OR'
    q2.children.append(("id", 0))
    for UserAccountChainYen in UserAccountChainYenInfo.objects.filter(q1):
        q2.children.append(("id", UserAccountChainYen.UserAccountInfo.id))
    # UserAccountChainYen = UserAccountChainYenInfo.objects.filter(q1)
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    if registerDDandDimInfo.objects.filter(amwayNumber = UserAccount.useraccountamwayinfo_set.first().amwayNumber).count() > 0:
        for UserAccountAmway in UserAccountAmwayInfo.objects.filter(amwayDD=UserAccount.useraccountamwayinfo_set.first().amwayNumber):
            q2.children.append(("id", UserAccountAmway.UserAccountInfo.id))
    searchUserAccountInfo = UserAccountInfo.objects.filter(q2)
    return render(request, 'managerPages/managerAccountManagerPage.html', locals())


@permission_required('userlogin.seeManagerAuditAccountPage', login_url='/accounts/userlogin/')
def managerAuditAccountPage(request):
    tag = "ManagerAuditAccountPage"

    # 職務表
    jobTitles = chainYenJobTitleInfo.objects.all()
    # 獎銜表
    amwayAwards = amwayAwardInfo.objects.all().order_by('rank')
    # 教室表
    chainYenClasses = chainYenClassInfo.objects.all().order_by('rank')
    # 白金表
    registerDDs = registerDDandDimInfo.objects.filter(amwayAward__rank__gte=15)
    # 鑽石表
    registerDims = registerDDandDimInfo.objects.filter(amwayAward__rank__gte=60)

    TempUserAccountChainYen = TempUserAccountChainYenInfo.objects.all()
    # print(TempUserAccount)
    # kwargs = {}
    # 台北
    if not request.user.has_perm('userlogin.CYPManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="台北")

    if not request.user.has_perm('userlogin.CYLManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="中壢")

    if not request.user.has_perm('userlogin.CYSManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="新竹")

    if not request.user.has_perm('userlogin.CYZManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="台中")

    if not request.user.has_perm('userlogin.CYJManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="嘉義")

    if not request.user.has_perm('userlogin.CYN2Manager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="永康245")

    if not request.user.has_perm('userlogin.CYN1Manager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="永康135")

    if not request.user.has_perm('userlogin.CYMManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="良美")

    if not request.user.has_perm('userlogin.CYKManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="高雄")

    if not request.user.has_perm('userlogin.CYDManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="屏東")

    if not request.user.has_perm('userlogin.CYWManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="花蓮")

    if not request.user.has_perm('userlogin.CYTManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="台東")

    if not request.user.has_perm('userlogin.CYHManager'):
        TempUserAccountChainYen = TempUserAccountChainYen.exclude(classRoom__ClassRoomName="澎湖")

    return render(request, 'managerPages/managerAuditAccountManagerPage.html', locals())


@permission_required('userlogin.seeManagerAuditAccountPage', login_url='/accounts/userlogin/')
def removeAuditAccount(request):
    response_data = {}

    try:
        tempAccountId = int(json.loads(request.body.decode('utf-8'))["id"])
        userAccount = TempUserAccountInfo.objects.filter(id=tempAccountId)
        confirm = ConfirmString.objects.filter(user_name=userAccount.first().username)
        if confirm.count()>0:
            confirm.delete()

        if userAccount.count()>0:
            userAccount.first().delete()

        response_data["status"] = True
    except:
        response_data["status"] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")


    return HttpResponse(json.dumps(response_data), content_type="application/json")


@permission_required('userlogin.seeManagerAuditAccountPage', login_url='/accounts/userlogin/')
def AcceptAuditAccount(request):
    response_data = {}

    try:
        tempAccountId = int(json.loads(request.body.decode('utf-8'))["id"])
        TempUserAccount = TempUserAccountInfo.objects.get(id=tempAccountId)
        code = make_confirm_string(TempUserAccount.username)
        send_email(TempUserAccount.email, code)

        TempUserAccount.auditStatus = "確認中"
        TempUserAccount.save()
        response_data["status"] = True

    except:
        response_data["status"] = False
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@permission_required('userlogin.seeManagerPointPage', login_url='/accounts/userlogin/')
def managerPointManagerPage(request):
    tag = "ManagerPointManagerPage"

    # 職務表
    jobTitles = chainYenJobTitleInfo.objects.all()
    # 獎銜表
    amwayAwards = amwayAwardInfo.objects.all().order_by('rank')
    # 教室表
    chainYenClasses = chainYenClassInfo.objects.all().order_by('rank')
    # 白金表
    registerDDs = registerDDandDimInfo.objects.filter(amwayAward__rank__gte=15)
    # 鑽石表
    registerDims = registerDDandDimInfo.objects.filter(amwayAward__rank__gte=60)

    q1 = Q()
    q1.connector = 'OR'
    q1.children.append(("classRoom__ClassRoomName", "無"))

    if request.user.has_perm('userlogin.CYPManager'):
        q1.children.append(("classRoom__ClassRoomName", "台北"))

    if request.user.has_perm('userlogin.CYLManager'):
        q1.children.append(("classRoom__ClassRoomName", "中壢"))

    if request.user.has_perm('userlogin.CYSManager'):
        q1.children.append(("classRoom__ClassRoomName", "新竹"))

    if request.user.has_perm('userlogin.CYZManager'):
        q1.children.append(("classRoom__ClassRoomName", "台中"))

    if request.user.has_perm('userlogin.CYJManager'):
        q1.children.append(("classRoom__ClassRoomName", "嘉義"))

    if request.user.has_perm('userlogin.CYN2Manager'):
        q1.children.append(("classRoom__ClassRoomName", "永康245"))

    if request.user.has_perm('userlogin.CYN1Manager'):
        q1.children.append(("classRoom__ClassRoomName", "永康135"))

    if request.user.has_perm('userlogin.CYMManager'):
        q1.children.append(("classRoom__ClassRoomName", "良美"))

    if request.user.has_perm('userlogin.CYKManager'):
        q1.children.append(("classRoom__ClassRoomName", "高雄"))

    if request.user.has_perm('userlogin.CYDManager'):
        q1.children.append(("classRoom__ClassRoomName", "屏東"))

    if request.user.has_perm('userlogin.CYWManager'):
        q1.children.append(("classRoom__ClassRoomName", "花蓮"))

    if request.user.has_perm('userlogin.CYTManager'):
        q1.children.append(("classRoom__ClassRoomName", "台東"))

    if request.user.has_perm('userlogin.CYHManager'):
        q1.children.append(("classRoom__ClassRoomName", "澎湖"))

    q2 = Q()
    q2.connector = 'OR'
    q2.children.append(("id", 0))
    for UserAccountChainYen in UserAccountChainYenInfo.objects.filter(q1):
        q2.children.append(("id", UserAccountChainYen.UserAccountInfo.id))
    # UserAccountChainYen = UserAccountChainYenInfo.objects.filter(q1)
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    if registerDDandDimInfo.objects.filter(amwayNumber = UserAccount.useraccountamwayinfo_set.first().amwayNumber).count() > 0:
        for UserAccountAmway in UserAccountAmwayInfo.objects.filter(amwayDD=UserAccount.useraccountamwayinfo_set.first().amwayNumber):
            q2.children.append(("id", UserAccountAmway.UserAccountInfo.id))
    #searchUserAccountInfo = UserAccountInfo.objects.filter(q2)
    searchUserAccountInfo = UserAccountInfo.objects.all()
    return render(request, 'managerPages/managerPointManagerPage.html', locals())


