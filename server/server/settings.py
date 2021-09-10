"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x%#0uep5b^^gqkfctv1=w6nasd$-j$eam*u*!#)7k-3dp)6t-4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# celery
CELERY_CACHE_BACKEND = 'celery'
CELERY_BROKER_URL = 'redis://localhost:6379'
CACHES = {
    'celery': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'celery_cache',
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'celery_cache',
    }
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',
    # Add our new application
    'searchfile',
    'NutriliteSearchPage',
    'userlogin',
    'personalInfoPage',
    'managerPage',
    'managerPage.templatetags',
    'pointManage',
    # plug-in
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db1', # DB名稱
        'USER': 'devuser2', # 使用者帳號
        'PASSWORD': 'chainyen', # 使用者密碼
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'userlogin.UserAccountInfo'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # another directory ...
]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#60 * 60
SESSION_COOKIE_AGE = 60*60*24  # 設置session過期時間為30分鐘
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 當瀏覽器被關閉的時候將session失效，但是不能刪除數據庫的session數據
SESSION_SAVE_EVERY_REQUEST = False  # 每次請求都要保存一下session

# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  #SMTP伺服器
EMAIL_PORT = 587  #TLS通訊埠號
EMAIL_USE_TLS = True  #開啟TLS(傳輸層安全性)
EMAIL_HOST_USER = 'ChainYenRetrieve@gmail.com'  #寄件者電子郵件
EMAIL_HOST_PASSWORD = 'dxuzkjluwqxbryox'  #Gmail應用程式的密碼
CONFIRM_DAYS = 3
MYIP = "http://1.34.134.127:12000"

CLASS_CHARIMAN_MANAGER_DICT = {
            "台北":"CYPManager",
            "中壢": "CYLManager",
            "新竹": "CYSManager",
            "台中": "CYZManager",
            "嘉義": "CYJManager",
            "永康245": "CYN2Manager",
            "永康135": "CYN1Manager",
            "良美": "CYMManager",
            "高雄": "CYKManager",
            "屏東": "CYDManager",
            "花蓮": "CYWManager",
            "台東": "CYTManager",
            "澎湖": "CYHManager"
}


