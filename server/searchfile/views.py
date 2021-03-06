from django.shortcuts import render
import logging
from userlogin.models import amwayAwardInfo ,chainYenJobTitleInfo ,chainYenClassInfo , UserAccountInfo , UserAccountChainYenInfo,UserAccountAmwayInfo

# Create your views here.
def home(request):
    

    AccountUser = UserAccountInfo.objects.get(username=request.user).user

    try:
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccountInfo.objects.get(username=request.user))
        amwayMember = UserAccountAmwayInfo.objects.get(
            UserAccountInfo=UserAccountInfo.objects.get(username=request.user)).amwayNumber

        classRoomCode = UserAccountChainYen.classRoom.ClassRoomCode
        name = classRoomCode +  "_" + AccountUser
    except:
        name = AccountUser
        amwayMember = ""
    s = render(request, 'home.html', locals())
    s.setdefault('Cache-Control', 'no-store')
    s.setdefault('Expires', 0)
    s.setdefault('Pragma', 'no-cache')
    return s

