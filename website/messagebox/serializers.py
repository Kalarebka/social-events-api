from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=User.objects.all()
    )
    sender_username = serializers.SerializerMethodField("get_sender_username")
    receiver_username = serializers.SerializerMethodField("get_receiver_username")

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
            "sender_username",
            "receiver_username",
        ]
        read_only_fields = ["id", "sender", "date_sent"]

    def get_sender_username(self):
        return self.sender.username

    def get_receiver_username(self):
        return self.receiver.username
