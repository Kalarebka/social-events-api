from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import BasicInvitation, BasicEmailInvitation


class BasicInvitationSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = BasicInvitation
        fields = [
            "id",
            "sender",
            "receiver",
            "confirmed",
            "response_received",
            "date_sent",
        ]
        read_only_fields = ["id", "confirmed", "response_received", "date_sent"]


class BasicEmailInvitationSerializer(BasicInvitationSerializer):
    class Meta(BasicInvitationSerializer.Meta):
        model = BasicEmailInvitation
