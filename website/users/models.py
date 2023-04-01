from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from invitations.base_models import AbstractEmailInvitation


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True, null=False, blank=False)
    username = models.CharField(
        "username", max_length=56, unique=True, null=False, blank=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    profile_picture = models.ImageField(
        default="default.jpg", upload_to="profile_images", blank=True
    )
    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.username

    class Meta:
        # Order alphabetically by username
        ordering = ["username"]


class UserGroup(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    administrators = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="administered_usergroups"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="usergroups"
    )
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FriendInvitation(AbstractEmailInvitation):
    def confirm(self):
        self.sender.friends.add(self.receiver)
        self.receiver.friends.add(self.sender)

    def get_email_template(self) -> str:
        return "invitation_emails/friend_invitation.html"

    def get_email_data(self):
        data = {}
        data["receiver_name"] = self.receiver.username
        data["sender_name"] = self.sender.username
        data["confirm_url"] = self.get_response_url("accept")
        data["decline_url"] = self.get_response_url("decline")
        return data

    def get_subject(self):
        return f"You have been invited to {self.sender.username}'s friends"

    def get_recipient_list(self):
        return [
            self.receiver.email,
        ]

    def get_response_url(self, invitation_response):
        url = reverse("users:friend_invite_email_response")
        response_url = (
            f"{url}?token={self.email_response_token}&response={invitation_response}"
        )
        return response_url


class GroupInvitation(AbstractEmailInvitation):
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name="invitations"
    )

    def confirm(self):
        self.group.members.add(self.receiver)

    def get_email_template(self) -> str:
        return "invitation_emails/group_invitation.html"

    def get_email_data(self):
        data = {}
        data["receiver_name"] = self.receiver.username
        data["group_name"] = self.group.name
        data["confirm_url"] = self.get_response_url("accept")
        data["decline_url"] = self.get_response_url("decline")
        return data

    def get_subject(self):
        return f"You have been invited to {self.group.name} group"

    def get_recipient_list(self):
        return [
            self.receiver.email,
        ]

    def get_response_url(self, invitation_response):
        url = reverse("users:group_invite_email_response")
        response_url = (
            f"{url}?token={self.email_response_token}&response={invitation_response}"
        )
        return response_url
