from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo,mainClassInfo,secClassInfo,personalFileData,personalExchangeFileLog
from userlogin.models import UserAccountInfo,UserAccountChainYenInfo, UserAccountAmwayInfo, registerDDandDimInfo
from NutriliteSearchPage.utils.page import Pagination
from pointManage.models import pointHistory
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.

def personalInfoHomePage(request,selectTag):
    if selectTag == "總部會議":
        selectTag += "/活動"


    try:
        userAccount = UserAccountInfo.objects.get(username=request.user)
        dataPermissionsLevel = userAccount.dataPermissionsLevel
        if selectTag == "全部":
            personalFile = userAccount.personalfiledata_set.filter(fileDataID__permissionsLevel__lte=dataPermissionsLevel,
                                                                   fileDataID__visible=1).order_by('exchangeDate')
        else:
            personalFile = userAccount.personalfiledata_set.filter(fileDataID__permissionsLevel__lte=dataPermissionsLevel,
                                                                   fileDataID__visible=1,
                                                                   fileDataID__mainClass__mainClassName=selectTag).order_by(
                'exchangeDate')
    except:
        dataPermissionsLevel = -1
    # fileDatas = fileDataInfo.objects.filter(mainClass=mainClassInfo.objects.get(mainClassName=selectTag).id,
    #                                         secClass=secClassInfo.objects.get(secClassName=selectTag).id,
    #                                         visible=1,
    #                                         permissionsLevel__lte=dataPermissionsLevel).order_by('occurrenceDate')
    fileDatas = personalFile
    # 總頁數
    page_count = fileDatas.count()
    pageisNotNull = True
    if page_count == 0:
        pageisNotNull = False
    # 當前頁
    current_page_num = request.GET.get("page")
    pagination = Pagination(current_page_num, page_count, request, per_page_num=10)
    # 處理之後的資料
    fileDatas = fileDatas[pagination.start:pagination.end]
    selectPage = "瀏覽已兌換資料"
    content = {
        "fileDatas": fileDatas, "pagination": pagination, }


    return render(request, 'personalInfoPages/personalInfoHomePage.html', locals())


def personalInfoPointPage(request):

    userAccountInfo = UserAccountInfo.objects.get(username = request.user.username)

    #紀錄
    pHistory = pointHistory.objects.filter(UserAccountInfo = userAccountInfo).order_by('-recordDate')

    #轉讓: 白金小組 & 鑽石小組
    myTeam = []
    userAccountAmway = UserAccountAmwayInfo.objects.get(UserAccountInfo = userAccountInfo)
    awardRank = userAccountAmway.amwayAward.rank
    amNumber  = userAccountAmway.amwayNumber
    #白金
    if awardRank >= 15 and awardRank < 60:
        myDDInfo = registerDDandDimInfo.objects.get(amwayNumber = amNumber)
        myTeam = UserAccountAmwayInfo.objects.filter(amwayDD = myDDInfo).values('UserAccountInfo').exclude(username = request.user.username)
    #鑽石
    elif awardRank >= 60:
        myDDInfo = registerDDandDimInfo.objects.get(amwayNumber = amNumber)
        accountIDList = UserAccountAmwayInfo.objects.filter(amwayDD = myDDInfo).values('UserAccountInfo')
        myTeam = UserAccountInfo.objects.filter(id__in=accountIDList).exclude(username = request.user.username)
        myTeamDD = registerDDandDimInfo.objects.filter(amwayDiamond = str(amNumber))
        for myDD in myTeamDD:
            accountIDList = UserAccountAmwayInfo.objects.filter(amwayDD = myDD).values('UserAccountInfo')
            myTeam = myTeam + UserAccountInfo.objects.filter(id__in=accountIDList).exclude(username = request.user.username)
    else:
        myTeam = []
    selectPage = "管理個人點數"

    return render(request, 'personalInfoPages/personalInfoPointPage.html', locals())



def changePasswordPage(request):

    return render(request, 'personalInfoPages/changePasswordPage.html', locals())


def changePasswordOption(request):
    password1 = request.POST.get("id_password1")
    password2 = request.POST.get("id_password2")
    password_old = request.POST.get("id_password_old")

    if password1 == password2:
        userAccountInfo = UserAccountInfo.objects.get(username=request.user.username)

        if check_password(password_old,userAccountInfo.password):
            userAccountInfo.password = make_password(password1)

            userAccountInfo.save()
            message = "成功修改密碼，五秒後跳轉到登入畫面"
        else:
            message = "修改失敗，舊密碼錯誤，五秒後跳轉到登入畫面"
    else:
        message = "修改失敗，發生錯誤，五秒後跳轉到登入畫面"

    # make_password(id_password1)
    #

    return render(request, 'personalInfoPages/changePasswordOptionResult.html', locals())
