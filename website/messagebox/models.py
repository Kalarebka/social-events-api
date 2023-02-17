from django.conf import settings
from django.db import models


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
    content = models.TextField(default="")
    date_sent = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_receiver = models.BooleanField(default=False)

    class Meta:
        # Order by date_sent descending
        ordering = ["-date_sent"]

    def __str__(self):
        return self.title


class MessageTemplate(models.Model):
    # templates to be used when creating auto messages
    # in db or in text files in static?
    pass
