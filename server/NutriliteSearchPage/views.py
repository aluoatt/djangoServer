from django.shortcuts import render
from NutriliteSearchPage.models import fileDataInfo,mainClassInfo,secClassInfo,fileTypeInfo,sourceFromInfo,fileDataKeywords
import logging
# Create your views here.
def NutriliteSearchPage(request,selectTag):
    selectTag = selectTag
    fileDatas = fileDataInfo.objects.filter(mainClass = mainClassInfo.objects.get(mainClassName="營養").id,
                                           secClass = secClassInfo.objects.get(secClassName=selectTag).id,
                                           visible = 1).order_by('occurrenceDate')


    return render(request, 'nutritionSearchPage.html', locals())
