from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')  # 設定django環境

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')  # 使用CELERY_ 作為字首，在settings中寫配置

app.autodiscover_tasks()  # 發現任務檔案每個app下的task.py