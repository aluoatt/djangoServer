from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo,mainClassInfo,secClassInfo,fileTypeInfo,sourceFromInfo,fileDataKeywords
from userlogin.models import UserAccountInfo,UserAccountChainYenInfo
from NutriliteSearchPage.utils.page import Pagination

import logging
# Create your views here.
def NutriliteSearchPage(request,selectTag):
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

    return render(request, 'nutritionSearchPage.html', locals())
