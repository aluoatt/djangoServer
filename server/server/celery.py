from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from kombu import Queue


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')  # 設定django環境

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')  # 使用CELERY_ 作為字首，在settings中寫配置

 # 路由
app.conf.task_routes = {'NutriliteSearchPage.tasks.getFileDateProcess': {'queue': 'celery_with_mark'},
                        'NutriliteSearchPage.tasks.getFileWithoutWaterProcess': {'queue': 'celery_with_out_mark'}}

# 配置默认队列， 若存在没有指定路由的， 将指定给默认队列
app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default', routing_key='default'),
    Queue('timing_one', routing_key='celery_with_mark'),
    Queue('timing_two', routing_key='celery_with_out_mark'),

)

app.autodiscover_tasks()  # 發現任務檔案每個app下的task.py