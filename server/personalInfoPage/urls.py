from django.urls import path
from . import views


urlpatterns = [
    path('personalRewardReport', views.personalRewardReport, name='personalRewardReport'),
    path('getSelfRewardReport', views.getSelfRewardReport, name='getSelfRewardReport'),
    path('rewardReportByExcel', views.rewardReportByExcel, name='rewardReportByExcel'),
]
