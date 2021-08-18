from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo,mainClassInfo,secClassInfo,personalFileData,personalExchangeFileLog
from userlogin.models import UserAccountInfo,UserAccountChainYenInfo
from NutriliteSearchPage.utils.page import Pagination
import logging
from .tasks import getFileDateProcess


# Create your views here.
# 查詢檔案
def NutriliteSearchPage(request,topic,selectTag):
    selectTag = selectTag
    try:
        dataPermissionsLevel = UserAccountInfo.objects.get(username=request.user).dataPermissionsLevel
        userpoint = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccountInfo.objects.get(username=request.user)).point

    except:
        userpoint = 0
        dataPermissionsLevel = -1

    fileDatas = fileDataInfo.objects.filter(mainClass = mainClassInfo.objects.get(mainClassName="營養").id,
                                           secClass = secClassInfo.objects.get(secClassName=selectTag).id,
                                           visible = 1,
                                           permissionsLevel__lte = dataPermissionsLevel).order_by('occurrenceDate')
    # 總頁數
    page_count = fileDatas.count()
    pageisNotNull = True
    if page_count == 0:
        pageisNotNull = False
    # 當前頁
    current_page_num = request.GET.get("page")
    pagination = Pagination(current_page_num, page_count,request, per_page_num=10)
    # 處理之後的資料
    fileDatas = fileDatas[pagination.start:pagination.end]

    content = {
        "fileDatas": fileDatas, "pagination": pagination, }

    return render(request, 'MainSearchPage.html', locals())

def viewFilePage(request,fileId):
    
    targetFile = fileDataInfo.objects.get(id=int(fileId))
    UserAccount = UserAccountInfo.objects.get(username=request.user)
    aleardyExchange = personalFileData.objects.filter(ownerAccount=UserAccount.id).count() > 0

    if request.user == "administrator":
        permission = True
        pointEnough = True
        supervisord = True
    else:
        #是否兌換

        supervisord = False
        UserAccountChainYen = UserAccountChainYenInfo.objects.get(UserAccountInfo=UserAccount)
        permission = targetFile.permissionsLevel <= UserAccount.dataPermissionsLevel
        #還沒兌換
        if not aleardyExchange:
            pointEnough = targetFile.point <= UserAccountChainYen.point
        else:
            pointEnough = True

    if (not permission) or (not pointEnough):
        targetFile = ""
        return render(request, 'viewFilePage.html', locals())

    if not supervisord:
        UserAccountChainYen.point = UserAccountChainYen.point - targetFile.point
        # UserAccountChainYen.save()
    if not aleardyExchange:
        # personalFileData(fileDataID=targetFile,
        #                  ownerAccount=UserAccount,
        #                  expiryDate=None,
        #                  costPoint=targetFile.point,
        #                  waterCreateReady=0,
        #                  ).save()
        #
        # personalExchangeFileLog(fileDataID=targetFile,
        #                         ownerAccount=UserAccount,
        #                         costPoint=targetFile.point,
        #                         ).save()
        if not supervisord:
            waterMarkUserName = UserAccountChainYen.classRoom.ClassRoomCode + "_" + UserAccount.user + "_"  \
                                + str(UserAccount.useraccountamwayinfo_set.all().first().amwayNumber)
            if targetFile.fileType.id > 1:# 非影片
                getFileDateProcess.delay(targetFile.PDF,waterMarkUserName,"pdf")
            else:
                getFileDateProcess.delay(targetFile.PDF,waterMarkUserName, "pdf")
        else:
            if targetFile.fileType.id > 1:  # 非影片
                getFileDateProcess.delay(targetFile.PDF,"超級使用者", "PDF")
            else:
                getFileDateProcess.delay(targetFile.PDF,"超級使用者", "PDF")
    # 發請求


    return render(request, 'viewFilePage.html', locals())