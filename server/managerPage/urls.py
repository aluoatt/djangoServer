from django.urls import path
from . import views


urlpatterns = [
    path('allUserAccount', views.allUserAccount, name='allUserAccount'),
    path('getTempUserAccount', views.getTempUserAccount, name='getTempUserAccount'),
    path('getFileDataSummary', views.getFileDataSummary, name='getFileDataSummary'),
]

