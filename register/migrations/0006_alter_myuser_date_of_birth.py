# Generated by Django 3.2.8 on 2021-12-24 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_myuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_of_birth',
            field=models.DateTimeField(),
        ),
    ]
