"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from searchfile.views import home
from django.conf.urls import url
from NutriliteSearchPage.views import NutriliteSearchPage,viewFilePage,returnPDF,exchangeOption,keywordSearchPage,returnFileStatus
from django .contrib.auth.decorators import login_required
from userlogin.views import login,logout,register,createRegisterPage,checkRegDD,registerSuccess
from personalInfoPage.views import personalInfoHomePage, personalInfoPointPage,changePasswordPage,changePasswordOption
from managerPage.views import managerAccountManagerPage,managerAuditAccountPage,removeAuditAccount,AcceptAuditAccount
from managerPage.views import userAccountConfirm,managerAccountModify,modalAccountModifyPOST
from managerPage.views import managerPointManagerPage,getAccountModifyHistory
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.views.generic.base import RedirectView

urlpatterns+=[
    url(r'^home', login_required(home)),
    # url("/", login_required(home)),
    # url(r'^home/NutriliteSearchPage/<str:selectTag>', NutriliteSearchPage),
]


urlpatterns += [
    path('home', login_required(home), name='home'),
    path('accounts/login/', login, name='login'),
    path('accounts/logout/', logout, name='logout'),
    path('accounts/registerSuccessStatus/<str:status>', registerSuccess, name='registerSuccess'),
    path('accounts/register/<str:token>', register,name='register'),
    path('accounts/createRegisterPage/', createRegisterPage,name='createRegisterPage'),

    path('filesearch/<str:topic>/<str:selectTag>', login_required(NutriliteSearchPage), name='NutriliteSearchPage'),

    path('viewFilePage/<str:fileId>', login_required(viewFilePage), name='viewFilePage'),
    path('keywordSearchPage', login_required(keywordSearchPage), name='keywordSearchPage'),

    path('returnPDF/<str:fileId>', login_required(returnPDF), name='returnPDF'),
    path('returnFileStatus/<str:fileId>', login_required(returnFileStatus), name='returnFileStatus'),
    path('exchangeOption/<str:fileId>', login_required(exchangeOption), name='exchangeOption'),
    path('personalInfoPage/home/<str:selectTag>', login_required(personalInfoHomePage), name='personalInfoHomePage'),
    path('personalInfoPage/pointPage', login_required(personalInfoPointPage), name='personalInfoPointPage'),
    path('personalInfoPage/changePasswordPage', login_required(changePasswordPage), name='changePasswordPage'),
    path('personalInfoPage/changePasswordOption', login_required(changePasswordOption), name='changePasswordOption'),

    path('managerPages/home/accountManger', login_required(managerAccountManagerPage), name='managerAccountManagerPage'),
    path('managerPages/home/AuditManger', login_required(managerAuditAccountPage),name='managerAuditAccountPage'),
    path('managerPages/home/PointManager', login_required(managerPointManagerPage),name='managerPointManagerPage'),
    path('managerPages/removeAuditAccount', login_required(removeAuditAccount),name='removeAuditAccount'),
    path('managerPages/AcceptAuditAccount', login_required(AcceptAuditAccount),name='AcceptAuditAccount'),
    path('managerPages/userAccountConfirm', userAccountConfirm,name='userAccountConfirm'),
    path('managerPages/managerAccountModify',managerAccountModify,name='managerAccountModify'),
    path('managerPages/modalAccountModifyPOST',modalAccountModifyPOST,name='modalAccountModifyPOST'),
    path('managerPages/getAccountModifyHistory',getAccountModifyHistory,name='getAccountModifyHistory'),


    path('checkRegDD', checkRegDD, name='checkRegDD'),

    path('', login_required(home), name='home'),
]

# Use include() to add paths from the catalog application
from django.conf.urls import include

urlpatterns += [
    path('pointManage/', include('pointManage.urls')),
]


# from django.views.generic import RedirectView
# urlpatterns += [
#     path('', RedirectView.as_view(url='/searchfile/')),
# ]
#
# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
