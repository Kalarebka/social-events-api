# Generated by Django 4.1.3 on 2023-03-07 18:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='administrators',
            field=models.ManyToManyField(related_name='administered_usergroups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='members',
            field=models.ManyToManyField(related_name='usergroups', to=settings.AUTH_USER_MODEL),
        ),
    ]
