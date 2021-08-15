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
from NutriliteSearchPage.views import NutriliteSearchPage
from django .contrib.auth.decorators import login_required
from userlogin.views import login,logout,register

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns+=[
    url(r'^home', login_required(home)),
    # url("/", login_required(home)),
    # url(r'^home/NutriliteSearchPage/<str:selectTag>', NutriliteSearchPage),
]


urlpatterns += [
    path('home', login_required(home), name='home'),

    path('accounts/login/', login, name='login'),
    path('accounts/logout/', logout, name='logout'),
    path('accounts/register/', register,name='register'),
    path('NutriliteSearchPage/<str:selectTag>', login_required(NutriliteSearchPage), name='NutriliteSearchPage'),
    path('', login_required(home), name='home'),
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