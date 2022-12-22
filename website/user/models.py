from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models

from event.models import Event, Location

from .user_manager import CustomUserManager


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["username"]

    profile_picture = models.ImageField(
        default="default.jpg", upload_to="profile_images", blank=True
    )
    events = models.ManyToManyField(Event)
    friends = models.ManyToManyField("self")
    favorite_locations = models.ManyToManyField(Location)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    name: models.TextField = models.TextField(max_length=128)
    administrators: models.ManyToManyField = models.ManyToManyField(User)
    members: models.ManyToManyField = models.ManyToManyField(
        User, related_name="user_groups"
    )


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    title = models.CharField(max_length=258, default="No title")
    content = models.TextField(default="")
    date_sent = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)


class Invitation(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_friend_invitations",
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_friend_invitations"
    )
    confirmed = models.BooleanField(default=False)

    def send_invitation(self):
        # Create a message with invitation + notification email (celery)
        pass

    def confirm_invitation(self):
        # can be confirmed by the receiver
        # only then: add the users to each other's friends
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
