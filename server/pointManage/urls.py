from django.urls import path
from . import views


urlpatterns = [
    path('addPoint', views.addPoint, name='addPoint'),
    path('addPointByAll', views.addPointByAll, name='addPointByAll'),
    path('addReducePointByUser', views.addReducePointByUser, name='addReducePointByUser'),
    path('addPointByAmwayAward', views.addPointByAmwayAward, name='addPointByAmwayAward'),
    path('addPointByJobTitle', views.addPointByJobTitle, name='addPointByJobTitle'),
    path('addPointByExcel', views.addPointByExcel, name='addPointByExcel'),
    path('addPointByCondition', views.addPointByCondition, name='addPointByCondition'),
    path('reducePoint', views.reducePoint, name='reducePoint'),
    path('getPointHistory', views.getPointHistory, name='getPointHistory'),
    path('getSelfPointHistory', views.getSelfPointHistory, name='getSelfPointHistory'),
    path('transferPoint', views.transferPoint, name='transferPoint'),
    path('allUserAccount', views.allUserAccount, name='allUserAccount'),
    path('getPersonalTeam', views.getPersonalTeam, name='getPersonalTeam'),
]

