from django.urls import path
from . import views


urlpatterns = [
    path('addPoint', views.addPoint, name='addPoint'),
    #path('addGroupPoint', views.addGroupPoint, name='addGroupPoint'),
    path('reducePoint', views.reducePoint, name='reducePoint'),
    path('getPointHistory', views.getPointHistory, name='getPointHistory'),
    path('transferPoint', views.transferPoint, name='transferPoint'),
]

