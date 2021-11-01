import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from recommendIndex.models import recommendIndexInfo
from NutriliteSearchPage.models import mainClassInfo


def recommendIndexHome(request):

    recommendIndexs = recommendIndexInfo.objects.all()
    mainClassAll = mainClassInfo.objects.all()


    return render(request, 'recommendIndexPages/recommendIndexPage.html', locals())

