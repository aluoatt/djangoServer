from django.urls import path
from . import views


urlpatterns = [
    path('addPoint', views.addPoint, name='addPoint'),
    path('addPointByAll', views.addPointByAll, name='addPointByAll'),
    path('addPointByAmwayAward', views.addPointByAmwayAward, name='addPointByAmwayAward'),
    path('addPointByJobTitle', views.addPointByJobTitle, name='addPointByJobTitle'),
    path('reducePoint', views.reducePoint, name='reducePoint'),
    path('getPointHistory', views.getPointHistory, name='getPointHistory'),
    path('transferPoint', views.transferPoint, name='transferPoint'),
    path('allUserAccount', views.allUserAccount, name='allUserAccount'),
]

