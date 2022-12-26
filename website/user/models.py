from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models

from .user_manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["username"]

    profile_picture = models.ImageField(
        default="default.jpg", upload_to="profile_images", blank=True
    )
    friends = models.ManyToManyField("self")

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    name: models.TextField = models.TextField(max_length=128)
    administrators: models.ManyToManyField = models.ManyToManyField(User)
    members: models.ManyToManyField = models.ManyToManyField(
        User, related_name="user_groups"
    )



class Invitation(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_sent",
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_received"
    )
    confirmed = models.BooleanField(default=False)

    def send_invitation(self):
        # Create a message with invitation + notification email (celery)
        pass

    def confirm_invitation(self):
        pass


    class Meta:
        abstract = True  # will not be used to create a db table


class FriendInvitation(Invitation):
    # how to change related_name for sender and receiver querysets?
    pass


class EventInvitation(Invitation):
    pass


class GroupInvitation(Invitation):
    pass
