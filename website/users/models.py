from typing import List

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    EmailField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    TextField,
)


class CustomUser(AbstractUser):
    email = EmailField("email address", unique=True, null=False, blank=False)
    username = CharField(
        "username", max_length=56, unique=True, null=False, blank=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["username"]

    profile_picture = ImageField(
        default="default.jpg", upload_to="profile_images", blank=True
    )
    friends = ManyToManyField("self")

    def __str__(self):
        return self.username


class UserGroup(Model):
    name: TextField = TextField(max_length=128)
    administrators: ManyToManyField = ManyToManyField(CustomUser)
    members: ManyToManyField = ManyToManyField(CustomUser, related_name="user_groups")


class AbstractInvitation(Model):
    sender = ForeignKey(
        CustomUser,
        on_delete=SET_NULL,
        null=True,
        related_name="%(app_label)s_%(class)s_sent",
    )
    receiver = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name="%(app_label)s_%(class)s_received",
    )
    confirmed = BooleanField(default=False)

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


class GroupInvitation(AbstractInvitation):
    pass
