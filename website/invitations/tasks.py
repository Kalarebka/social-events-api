from typing import List

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string

from .models import AbstractInvitation


@shared_task
def send_invitation_email(invitation: AbstractInvitation):
    email = create_invitation_email(invitation)
    email.send()


@shared_task
def send_batch_invitation_emails(invitation_list: List[AbstractInvitation]):
    email_messages = []
    for invitation in invitation_list:
        email = create_invitation_email(invitation)
        email_messages.append(email)

    connection = get_connection()
    connection.send_messages(email_messages)


def create_invitation_email(invitation: AbstractInvitation):
    email_template = invitation.email_template
    email_data = invitation.email_data

    subject = email_data.pop(subject, "No subject")
    recipient_list = [
        invitation.receiver.email,
    ]

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


# views.py
from django.shortcuts import render
from .tasks import send_invitation_email, send_many_invitation_emails


def create_invitation(request):
    # Code to create an invitation object
    invitation = GroupInvitation(sender=sender, receiver=receiver, group=group)
    invitation.save()

    # Call the send_invitation_email task for one invitation
    send_invitation_email.delay(invitation.pk)

    # Call the send_many_invitation_emails task for a list of invitations
    invitation_ids = [invitation.pk for invitation in invitations]
    send_many_invitation_emails.delay(invitation_ids)

    # Render the response
    return render(request, "create_invitation.html", {"invitation": invitation})
