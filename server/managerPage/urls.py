from django.urls import path
from . import views


urlpatterns = [
    path('allUserAccount', views.allUserAccount, name='allUserAccount'),
    path('getTempUserAccount', views.getTempUserAccount, name='getTempUserAccount'),
    path('getFileDataSummary', views.getFileDataSummary, name='getFileDataSummary'),
    path('getFileDataInfo', views.getFileDataInfo, name='getFileDataInfo'),
    path('updateFileDataInfo', views.updateFileDataInfo, name='updateFileDataInfo'),
    path('getArticleHistory', views.getArticleHistory, name='getArticleHistory'),
]

