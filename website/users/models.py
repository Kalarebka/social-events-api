from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from invitations.models import AbstractInvitation


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


class FriendInvitation(AbstractInvitation):
    def confirm(self):
        self.sender.friends.add(self.receiver)
        self.receiver.friends.add(self.sender)


class GroupInvitation(AbstractInvitation):
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name="invitations"
    )

    def confirm(self):
        self.group.members.add(self.receiver)
