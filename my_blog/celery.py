from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")
app = Celery("my_blog")
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace="CELERY")

# Celery Beat Settings
app.conf.beat_schedule = {
    'archive-exp-sub-by-celery': {
        'task': 'blogs.tasks.schedule_exp_sub',
        'schedule': crontab(hour=11, minute=43),
        #'args': (2,)
    }
}
app.conf.timezone = 'Asia/Kolkata'
app.autodiscover_tasks()
@app.task(bind=True)  
def debug_task(self):
    print(f'Request: {self.request!r}')