from django.contrib.auth import get_user_model
from rest_framework import serializers

from .db_helpers import get_message_thread
from .models import Message, MessageThread

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=User.objects.all()
    )
    sender_username = serializers.SerializerMethodField()
    receiver_username = serializers.SerializerMethodField()
    thread_id = serializers.PrimaryKeyRelatedField(source="thread", read_only=True)

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
            "thread_id",
        ]
        read_only_fields = ["id", "sender", "date_sent", "thread_id"]

    def get_sender_username(self, obj):
        return obj.sender.username

    def get_receiver_username(self, obj):
        return obj.receiver.username

    def create(self, validated_data):
        sender = validated_data["sender"]
        receiver = validated_data["receiver"]
        title = validated_data.get("title", "No title")
        content = validated_data.get("content", "")
        message_thread = get_message_thread(sender.id, receiver.id)
        if not message_thread:
            message_thread = MessageThread.objects.create(user1=sender, user2=receiver)
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            title=title,
            content=content,
            thread=message_thread,
        )
        return message


class MessageThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user1 = serializers.StringRelatedField()
    user2 = serializers.StringRelatedField()

    class Meta:
        model = MessageThread
        fields = ("id", "user1", "user2", "messages")
