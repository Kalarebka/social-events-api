from typing import List

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string

from .models import AbstractEmailInvitation


def create_invitation_email(invitation: AbstractEmailInvitation) -> EmailMessage:
    email_template = invitation.get_email_template()
    email_data = invitation.get_email_data()
    subject = invitation.get_subject()
    recipient_list = invitation.get_recipient_list()

    # Create message content from template
    content = render_to_string(email_template, context=email_data)

    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    return email


@shared_task
def send_invitation_email(invitation: AbstractEmailInvitation):
    email = create_invitation_email(invitation)
    email.send()


@shared_task
def send_batch_invitation_emails(invitation_list: List[AbstractEmailInvitation]):
    email_messages = []
    for invitation in invitation_list:
        email = create_invitation_email(invitation)
        email_messages.append(email)

    connection = get_connection()
    connection.send_messages(email_messages)
