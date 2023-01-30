# Generated by Django 4.1.3 on 2023-01-30 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_recurringeventschedule_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_access',
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('personal', 'Personal'), ('group', 'Group')], default='personal', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='organisers',
            field=models.ManyToManyField(related_name='events_as_organiser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events_as_participant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EventInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited_users', to='events.event')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_invitations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
