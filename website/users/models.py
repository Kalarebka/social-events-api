from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True, null=False, blank=False)
    username = models.CharField(
        "username", max_length=56, unique=True, null=False, blank=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["username"]

    profile_picture = models.ImageField(
        default="default.jpg", upload_to="profile_images", blank=True
    )
    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    name: models.TextField = models.TextField(max_length=128)
    administrators: models.ManyToManyField = models.ManyToManyField(CustomUser)
    members: models.ManyToManyField = models.ManyToManyField(
        CustomUser, related_name="user_groups"
    )


class AbstractInvitation(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_sent",
    )
    receiver = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_received",
    )
    confirmed = models.BooleanField(default=False)

    def send_invitation(self):
        # Create a message with invitation + notification email (celery)
        # some function to load message template
        # send message with messagebox
        # notification email in celery task
        pass

    def confirm_invitation(self):
        # self.confirmed = True
        pass

    class Meta:
        abstract = True  # will not be used to create a db table


class FriendInvitation(AbstractInvitation):
    pass


class EventInvitation(AbstractInvitation):
    pass


class GroupInvitation(AbstractInvitation):
    pass
