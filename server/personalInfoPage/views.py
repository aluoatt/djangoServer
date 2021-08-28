from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo,mainClassInfo,secClassInfo,personalFileData,personalExchangeFileLog
from userlogin.models import UserAccountInfo,UserAccountChainYenInfo
from NutriliteSearchPage.utils.page import Pagination
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

    content = {
        "fileDatas": fileDatas, "pagination": pagination, }


    return render(request, 'personalInfoPages/personalInfoHomePage.html', locals())