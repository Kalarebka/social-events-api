from django.conf import settings
from django.db import models


class MessageThread(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="thread_user1",
        on_delete=models.SET_NULL,
        null=True,
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="thread_user2",
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user1", "user2"]

    def __str__(self):
        return f"Messages between {self.user1} and {self.user2}"


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_messages",
    )
    title = models.CharField(max_length=258, default="No title")
    content = models.CharField(max_length=10000, default="")
    date_sent = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    date_read = models.DateTimeField(default=None, null=True, blank=True)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)
    thread = models.ForeignKey(
        MessageThread, on_delete=models.CASCADE, related_name="messages"
    )

    class Meta:
        # Order by date_sent descending
        ordering = ["-date_sent"]

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.title}"
