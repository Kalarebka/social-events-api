from typing import List
from uuid import uuid4

from django.conf import settings
from django.db import models


class AbstractInvitation(models.Model):
    """
    An abstract base class for invitations.

    The self.confirm method must be implemented with any actions that should be performed
    once the invitation is confirmed.
    """

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="%(app_label)s_%(class)s_sent",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_received",
    )
    confirmed = models.BooleanField(default=False)
    response_received = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

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


class AbstractEmailInvitation(AbstractInvitation):
    """
    An abstract base class for invitation that can be sent and receive response through e-mail.

    Additional attribute: Email response token - 128 bit UUID created when the invitation is first created,
    saved as 32 character hexadecimal str.
    """

    email_response_token = models.CharField(max_length=32, unique=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.token = uuid4().hex
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def get_email_template(self) -> str:
        # Return an html template path
        raise NotImplementedError()

    def get_email_data(self) -> dict:
        # Return a dictionary of values to substitute in email template
        raise NotImplementedError()

    def get_subject(self) -> str:
        # Return email subject (str)
        raise NotImplementedError()

    def get_recipient_list(self) -> List[str]:
        # Return recipient list. If there is only one recipient, return 1-element list
        raise NotImplementedError()

    def get_response_url(self, invitation_response) -> str:
        # Return a url to an endpoint receiving invitations responses, containing response and token
        # TODO should be possible to change to child classes only providing base url
        raise NotImplementedError()
