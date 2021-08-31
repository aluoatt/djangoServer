from django.urls import path
from . import views


urlpatterns = [
    path('addPoint', views.addPoint, name='addPoint'),
    path('reducePoint', views.reducePoint, name='reducePoint'),
    path('getPointHistory', views.getPointHistory, name='getPointHistory'),
]

