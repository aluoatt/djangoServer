from django.urls import path
from . import views


urlpatterns = [
    path('allUserAccount', views.allUserAccount, name='allUserAccount'),
    path('getTempUserAccount', views.getTempUserAccount, name='getTempUserAccount'),
    path('getFileDataSummary', views.getFileDataSummary, name='getFileDataSummary'),
    path('getFileDataInfo', views.getFileDataInfo, name='getFileDataInfo'),
    path('getFileDataInfoByID/<str:articleID>', views.getFileDataInfoByID, name='getFileDataInfoByID'),
    path('updateFileDataInfo', views.updateFileDataInfo, name='updateFileDataInfo'),
    path('getArticleHistory', views.getArticleHistory, name='getArticleHistory'),
    path('getArticleReport/<str:status>', views.getArticleReport, name='getArticleReport'),
    path('reportArticle', views.reportArticle, name='reportArticle'),
    path('removeArticleReport/<str:reportID>', views.removeArticleReport, name='removeArticleReport'),
    path('getArticleOwnRank', views.getArticleOwnRank, name='getArticleOwnRank'),
]

