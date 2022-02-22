# Generated by Django 3.2.11 on 2022-02-02 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0014_alter_myuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'ordering': ['username'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='name',
        ),
        migrations.AddField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Имя пользователя'),
        ),
    ]