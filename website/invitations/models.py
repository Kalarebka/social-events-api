from abc import ABC, abstractproperty
from uuid import uuid4

from django.conf import settings
from django.db import models


class AbstractInvitation(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="%(app_label)s_%(class)s_sent",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_received",
    )
    confirmed = models.BooleanField(default=False)
    response_received = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    # Email response token - 128 bit UUID saved as 32 character hexadecimal str
    email_response_token = models.CharField(max_length=32, unique=True)

    # Invitation email template
    @property
    def get_invitation_email_template(self):
        raise NotImplementedError(
            "Invitation email template property must be implemented."
        )

    def save(self, *args, **kwargs):
        #
        # When the invitation is first created, create invitation email and email_response_token
        # task to send the email will be called in view after creating invitation,
        # to be able to send many invitations at once
        if self._state.adding:
            self.token = uuid4().hex
            self.create_invitation_email()
        super().save(*args, **kwargs)

    def create_invitation_email(self):
        # Return InvitationEmail object containing urls to confirm and decline the invitation
        # with a confirmation token
        pass

    def send_response(self, response):
        if response == "accept":
            self.confirmed = True
            self.confirm()
        else:
            self.response_received = True

    def confirm(self):
        pass

    class Meta:
        abstract = True


class InvitationEmail(models.Model):
    sender = models.EmailField()
    receiver = models.EmailField()
    confirm_url = models.URLField()
    decline_url = models.URLField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
