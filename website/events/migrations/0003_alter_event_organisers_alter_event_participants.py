# Generated by Django 4.1.3 on 2023-03-07 12:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organisers',
            field=models.ManyToManyField(related_name='organised_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events', through='events.EventInvitation', to=settings.AUTH_USER_MODEL),
        ),
    ]