from django.test import TestCase

from ..models import MyUser
from ..tasks import user_is_notify_task


class TasksTestCase(TestCase):
    @classmethod
    def CreateNewUserTestCase(cls):
        MyUser.objects.create(name='vlad', email='vlad@gm.com', password='vlad', date_of_birth='1998-25-09')

    def test_for_user_is_notify_task(self):
        for user in MyUser.objects.all():
            self.assertTrue(user.is_notified)
        self.assertEqual(user_is_notify_task(), 'Все пользователи уведомлены')
