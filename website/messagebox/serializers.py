from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    PrimaryKeyRelatedField,
    ModelSerializer,
)

from .models import Message

User = get_user_model()


class MessageSerializer(ModelSerializer):
    sender = PrimaryKeyRelatedField(read_only=True)
    receiver = PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all())

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
        read_only_fields = ["id", "sender", "date_sent"]
