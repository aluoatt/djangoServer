import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from NutriliteSearchPage.models import fileDataInfo, personalFileData


def like_change(request):
    if request.GET.get('is_like') == 'true':
        is_like = True
    else:
        is_like = False

    fileid = request.GET.get('fileid')
    response_data = {}
    personalFileDataGet = personalFileData.objects.filter(ownerAccount=request.user, fileDataID=int(fileid))

    if personalFileDataGet.count() < 0:

        response_data["status"] = False

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        fileData = fileDataInfo.objects.filter(id=int(fileid)).first()
        personalFileDataGet = personalFileDataGet.first()

        if personalFileDataGet.like != is_like:
            personalFileDataGet.like = is_like
            if is_like:
                fileData.likes = fileData.likes + 1
            else:
                fileData.likes = fileData.likes - 1

            fileData.save()
            personalFileDataGet.save()

        response_data["status"] = True
        response_data["liked_num"] = fileData.likes
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def putStars(request):
    rates = float(request.GET.get('stars'))


    fileid = request.GET.get('fileid')
    response_data = {}
    personalFileDataGet = personalFileData.objects.filter(ownerAccount=request.user, fileDataID=int(fileid))

    if personalFileDataGet.count() < 0:

        response_data["status"] = False

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        fileData = fileDataInfo.objects.filter(id=int(fileid)).first()
        personalFileDataGet = personalFileDataGet.first()
        personalFileDataGet.getStar = 1
        personalFileDataGet.stars = rates
        personalFileDataGet.save()

        allThisFilepersonalFileData = personalFileData.objects.filter(fileDataID=int(fileid),getStar=1)


        totalstar = sum([i.stars for i in allThisFilepersonalFileData])/allThisFilepersonalFileData.count()

        fileData.stars = totalstar

        fileData.save()

        response_data["status"] = True
        response_data["stars_num"] = totalstar
        return HttpResponse(json.dumps(response_data), content_type="application/json")