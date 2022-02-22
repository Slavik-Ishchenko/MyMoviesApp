from celery import shared_task

from .models import MyUser

"""For start celery worker/beat I used this command: 'celery -A {name of app} worker --loglevel=info -P eventlet'.
   Having previously installed eventlet: 'pip install eventlet'"""

@shared_task
def user_is_notify_task():
    users_with_false_status = MyUser.objects.filter(is_notified=False)
    for user in users_with_false_status:
        if not user.is_notified:
            user.is_notified = True
            user.save()
        print(f'Пользователь {user.name} уведомлен')
    return "Все пользователи уведомлены"
