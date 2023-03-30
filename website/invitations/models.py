from django.urls import reverse

from .base_models import AbstractEmailInvitation, AbstractInvitation


class BasicInvitation(AbstractInvitation):
    """
    A basic implementation of invitation model
    """

    def confirm(self):
        # No additional actions when the invitation is confirmed
        pass


class BasicEmailInvitation(AbstractEmailInvitation):
    """
    A basic implementation of email invitation model
    """

    def confirm(self):
        # No additional actions when the invitation is confirmed
        pass

    def get_email_template(self):
        return "invitations/base_invitation_email.html"

    def get_email_data(self):
        data = {}
        data["sender_name"] = self.sender.username
        data["receiver_name"] = self.receiver.username
        data["accept_url"] = self.get_response_url("accept")
        data["decline_url"] = self.get_response_url("decline")
        return data

    def get_subject(self):
        return "You've received an invitation"

    def get_recipient_list(self):
        return [
            self.receiver.email,
        ]

    def get_response_url(self, invitation_response):
        url = reverse("invitations:email_response")
        response_url = (
            f"{url}?token={self.email_response_token}&response={invitation_response}"
        )
        return response_url
