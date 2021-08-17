from django.shortcuts import render

# Create your views here.
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from userlogin.models import amwayAwardInfo ,chainYenJobTitleInfo ,chainYenClassInfo , UserAccountInfo , UserAccountChainYenInfo,UserAccountAmwayInfo
import logging
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    username = request.POST.get('username', '')
    idnumber = request.POST.get('idnumber', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username + idnumber, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/home/')
    else:
        if username != '':

            pwderror = True
        return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@permission_required('userlogin.can_see_register', login_url='/accounts/userlogin/')
def register(request):
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
        chainYenJobTitle = int(request.POST.get('chainYenJobTitle', ''))
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
        r = UserAccountInfo.objects.create_user(username = accountName+IDnumber,
                            user=username,
                            gender = gander,
                            phone = phone,
                            password = id_password1,
                            is_superuser = 0,
                            is_staff =0,
                            is_active=1,
                            email=e_mail)

        r2 = UserAccountChainYenInfo(UserAccountInfo = r,
                                     jobTitle = chainYenJobTitleInfo.objects.get(id=chainYenJobTitle),
                                     classRoom = chainYenClassInfo.objects.get(classRoom=ChainYenClass),
                                     babysitter=babysitter,
                                     accountStatus="正常",
                                     freezeDate=None,
                                     point=0,
                                     EM=EM)

        r3 = UserAccountAmwayInfo(UserAccountInfo= r,
                                  amwayNumber=accountName,
                                  amwayAward=amwayAwardInfo.objects.get(amwayAward=amwayAward),
                                  amwayDD=amwayDD,

                                  amwayDiamond=amwayDiamond)

        r.save()
        r2.save()
        r3.save()
        #
        regSuccessnName = username
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
        e_mail = ''
        regSuccess = True
        return render(request, 'register.html', locals())

    else:
        form = UserCreationForm()
        amwayawards = amwayAwardInfo.objects.all()
        ChainYenJobTitles = chainYenJobTitleInfo.objects.all()
        ChainYenClassInfos = chainYenClassInfo.objects.all()
    return render(request, 'register.html', locals())