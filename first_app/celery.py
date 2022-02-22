import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_app.settings',)

app = Celery('register')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

"""For start celery worker/beat I used command 'celery -A {name of app} worker --loglevel=info -P eventlet'.
   Having previously installed eventlet 'pip install eventlet'"""

app.conf.beat_schedule = {
    'user-is-notify-task-every-day': {
        'task': 'register.tasks.user_is_notify_task',
        'schedule': crontab(minute=0, hour=12),  # every day
        # 'schedule': timedelta(seconds=15),  # for test
        # 'schedule': crontab(),  # every minute
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
