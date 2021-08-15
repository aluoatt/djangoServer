from django.shortcuts import render
import logging
from userlogin.models import amwayAwardInfo ,chainYenJobTitleInfo ,chainYenClassInfo , UserAccountInfo , UserAccountChainYenInfo,UserAccountAmwayInfo

# Create your views here.
def home(request):
    

    user = UserAccountInfo.objects.get(username=request.user).user

    try:
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccountInfo.objects.get(username=request.user))
        amwayMember = UserAccountAmwayInfo.objects.get(
            UserAccountInfo=UserAccountInfo.objects.get(username=request.user)).amwayNumber
        classRoomCode = UserAccountChainYen.classRoom.ClassRoomCode
        name = classRoomCode +  "_" + user +  "_" + UserAccountChainYen.babysitter
    except:
        name = user
        amwayMember = ""


    return render(request, 'home.html', locals())