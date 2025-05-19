import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuhes_shop.settings')
app = Celery('tuhes_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.worker_pool = 'solo'
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()