from typing import List

from celery import shared_task

from django.core.mail import EmailMessage, get_connection


@shared_task
def send_email_task(email: EmailMessage, email_backend):
    connection = get_connection(backend=email_backend)
    connection.send_messages(
        [
            email,
        ]
    )


@shared_task
def send_batch_email_task(email_list: List[EmailMessage], email_backend):
    connection = get_connection(backend=email_backend)
    connection.send_messages(email_list)
