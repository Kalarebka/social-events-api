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
    name = models.TextField(max_length=128)
    administrators = models.ManyToManyField(CustomUser, related_name="groups_as_admin")
    members = models.ManyToManyField(CustomUser, related_name="groups_as_member")


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
    declined = models.BooleanField(default=False)

    def send_invitation(self):
        # send a notification email to the receiver (celery task)
        # celery task function arguments: email template file, dict with args to insert into template
        # (sender, receiver, )
        pass

    def confirm_invitation(self):
        pass

    class Meta:
        abstract = True


class FriendInvitation(AbstractInvitation):
    def confirm_invitation(self):
        self.sender.friends.add(self.receiver)
        self.receiver.friends.add(self.sender)


class GroupInvitation(AbstractInvitation):
    group = models.ForeignKey(
        UserGroup, on_delete=models.CASCADE, related_name="invitations"
    )

    def confirm_invitation(self):
        self.group.members.add(self.receiver)
