from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_user_token(self, username, password):
        user = MyUser.objects.get_by_natural_key(username=username)
        if user.check_password(password):
            return Token.objects.get_or_create(user=user)


class MyUser(AbstractBaseUser):
    name = models.CharField('Имя пользователя', max_length=100, unique=True, null=True)
    email = models.EmailField('E-mail адрес', max_length=100, unique=True, null=True)
    password = models.CharField('Пароль', max_length=250, null=True)
    date_of_birth = models.DateTimeField('Дата рождения', null=True)
    is_notified = models.BooleanField('Уведомлен?', default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['name']
