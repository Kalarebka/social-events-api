# Generated by Django 4.1.3 on 2023-02-15 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_customuser_options_friendinvitation_date_sent_and_more"),
        ("events", "0003_remove_event_event_access_event_event_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventinvitation",
            name="confirmed",
        ),
        migrations.AddField(
            model_name="event",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.usergroup",
            ),
        ),
        migrations.AddField(
            model_name="eventinvitation",
            name="response",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("declined", "Declined"),
                ],
                default=1,
                max_length=15,
            ),
            preserve_default=False,
        ),
    ]