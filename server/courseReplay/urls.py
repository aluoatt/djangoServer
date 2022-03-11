from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='courseReplay_index'),
    path('viewFilePage/<str:fileId>', views.viewFilePage, name='viewFilePage'),
    path('returnVideo/<str:fileId>', views.returnVideo, name='returnVideo'),
    path('returnFileStatus/<str:fileId>', views.returnFileStatus, name='returnFileStatus'),
    path('confirmViewFileSubmit/<str:fileId>', views.confirmViewFileSubmit, name='confirmViewFileSubmit'),
    path('webvtt', views.webvtt, name='webvtt'),
]
