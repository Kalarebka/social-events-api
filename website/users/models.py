from abc import ABC, abstractproperty

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


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
        settings.AUTH_USER_MODEL, related_name="groups_as_admin"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="groups_as_member"
    )


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

    def save(self, *args, **kwargs):
        # When the invitation is first created, send and email with notification
        if self._state.adding:
            self.send_invitation_email()
        super().save(*args, **kwargs)

    def send_invitation_email(self):
        # send a notification email to the receiver (celery task)
        # celery task function arguments: email template file, dict with args to insert into template
        # (sender, receiver, )
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


class FriendInvitation(AbstractInvitation):
    def confirm(self):
        self.sender.friends.add(self.receiver)
        self.receiver.friends.add(self.sender)
        self.sender.save()
        self.receiver.save()


class GroupInvitation(AbstractInvitation):
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name="invitations"
    )

    def confirm(self):
        self.group.members.add(self.receiver)
        self.group.save()
