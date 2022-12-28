# Generated by Django 4.1.3 on 2022-12-26 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "event_access",
                    models.CharField(
                        choices=[
                            ("private", "Private"),
                            ("group", "Group"),
                            ("public", "Public"),
                        ],
                        max_length=8,
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField()),
                ("time_created", models.DateTimeField(auto_now_add=True)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("country", models.CharField(blank=True, max_length=32, null=True)),
                ("city", models.CharField(blank=True, max_length=32, null=True)),
                ("street", models.CharField(blank=True, max_length=32, null=True)),
                (
                    "street_number",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                ("zip_code", models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]