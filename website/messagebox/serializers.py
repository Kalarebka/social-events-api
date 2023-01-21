from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    CurrentUserDefault,
    PrimaryKeyRelatedField,
    ModelSerializer,
)

from .models import Message


class MessageSerializer(ModelSerializer):
    sender = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "title",
            "content",
            "date_sent",
            "read_status",
        ]
        read_only_fields = ["sender", "date_sent"]
