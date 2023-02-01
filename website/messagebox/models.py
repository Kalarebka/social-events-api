from django.conf import settings
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)


class Message(Model):
    sender = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        null=True,
        related_name="sent_messages",
    )
    receiver = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="received_messages",
    )
    title = CharField(max_length=258, default="No title")
    content = TextField(default="")
    date_sent = DateTimeField(auto_now_add=True)
    read_status = BooleanField(default=False)

    class Meta:
        # Order by date_sent descending
        ordering = ["-date_sent"]

    def __str__(self):
        return self.title


class MessageTemplate(Model):
    # templates to be used when creating auto messages
    # in db or in text files in static?
    pass
