# Generated by Django 3.2.8 on 2021-12-21 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20211218_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='preview',
            field=models.TextField(max_length=5000, verbose_name='Описание фильма'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название фильма'),
        ),
    ]