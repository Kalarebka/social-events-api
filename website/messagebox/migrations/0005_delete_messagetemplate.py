# Generated by Django 4.1.3 on 2023-02-22 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messagebox', '0004_message_deleted_by_receiver_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MessageTemplate',
        ),
    ]