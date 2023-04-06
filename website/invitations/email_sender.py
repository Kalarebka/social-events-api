from typing import List

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import AbstractEmailInvitation
from .tasks import send_email_task, send_batch_email_task


class EmailInvitationSender:
    def __init__(self, email_backend=None):
        self.email_backend = email_backend or getattr(
            settings, "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
        )

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

    def send_invitation(self, invitation: AbstractEmailInvitation):
        email = self.create_invitation_email(invitation)
        send_email_task.delay(email=email, backend=self.backend)

    def send_batch_invitation_email(
        self, invitation_list: List[AbstractEmailInvitation]
    ):
        email_messages = []
        for invitation in invitation_list:
            email = self.create_invitation_email(invitation)
            email_messages.append(email)
        send_batch_email_task.delay(email_list=email_messages, backend=self.backend)
