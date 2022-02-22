# Generated by Django 3.2.11 on 2022-02-02 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0015_auto_20220202_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'ordering': ['name'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='username',
        ),
        migrations.AddField(
            model_name='myuser',
            name='name',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Имя пользователя'),
        ),
    ]