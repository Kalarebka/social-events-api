from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import BasicEmailInvitation, BasicInvitation


class BasicInvitationSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = BasicInvitation
        fields = [
            "id",
            "sender",
            "recipient",
            "confirmed",
            "response_received",
            "date_sent",
        ]
        read_only_fields = ["id", "confirmed", "response_received", "date_sent"]


class BasicEmailInvitationSerializer(BasicInvitationSerializer):
    class Meta(BasicInvitationSerializer.Meta):
        model = BasicEmailInvitation
