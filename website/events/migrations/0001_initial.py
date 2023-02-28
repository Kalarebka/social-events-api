# Generated by Django 4.1.3 on 2023-02-28 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('private', 'Private Event'), ('group', 'Group Event')], max_length=15)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('in progress', 'In progress'), ('ended', 'Ended'), ('cancelled', 'Cancelled')], default='planned', max_length=11)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EventInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.BooleanField(default=False)),
                ('response_received', models.BooleanField(default=False)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('email_response_token', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('country', models.CharField(blank=True, max_length=32, null=True)),
                ('city', models.CharField(blank=True, max_length=32, null=True)),
                ('street', models.CharField(blank=True, max_length=32, null=True)),
                ('street_number', models.CharField(blank=True, max_length=8, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecurringEventSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.IntegerField()),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=10)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('repeats', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
