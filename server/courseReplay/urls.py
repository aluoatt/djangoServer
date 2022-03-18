from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name='courseReplay_index'),
    path('viewFilePage/<str:fileId>', login_required(views.viewFilePage), name='viewFilePage'),
    path('returnVideo/<str:fileId>', login_required(views.returnVideo), name='returnVideo'),
    path('returnFileStatus/<str:fileId>', login_required(views.returnFileStatus), name='returnFileStatus'),
    path('confirmViewFileSubmit/<str:fileId>', login_required(views.confirmViewFileSubmit), name='confirmViewFileSubmit'),
    path('webvtt', login_required(views.webvtt), name='webvtt'),
    path('confirmReplayVideo/<str:fileId>', login_required(views.confirmReplayVideo), name='confirmReplayVideo'),
]
