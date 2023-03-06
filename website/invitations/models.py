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

    # Invitation email properties
    @property
    def email_template(self):
        raise NotImplementedError()

    @property
    def email_data(self):
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        # When the invitation is first created, create email_response_token
        if self._state.adding:
            self.token = uuid4().hex
        super().save(*args, **kwargs)

    def send_response(self, response):
        if response == "accept":
            self.confirmed = True
            self.confirm()
        else:
            self.response_received = True

    def confirm(self):
        raise NotImplementedError()

    class Meta:
        abstract = True


class InvitationEmail(models.Model):
    sender = models.EmailField()
    receiver = models.EmailField()
    confirm_url = models.URLField()
    decline_url = models.URLField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
