from django.urls import reverse
from rest_framework import serializers

from .models import CustomUser, FriendInvitation, GroupInvitation, UserGroup


class UserProfileSerializer(serializers.ModelSerializer):
    """Public user profile information, for retrieve only views"""

    friend_ids = serializers.SerializerMethodField("get_friend_ids")

    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_picture", "friend_ids"]

    def get_friend_ids(self, obj):
        return [friend.id for friend in obj.friends.all()]


class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal user information, for retrieve only views"""

    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_url"]

    def get_profile_url(self, obj):
        return reverse("users:user_profile", kwargs={"pk": obj.pk})


class UserOwnProfileSerializer(UserProfileSerializer):
    """Adds private fields to profile serializer and allow updating the information"""

    class Meta:
        model = CustomUser
        fields = UserProfileSerializer.Meta.fields + ["email", "is_active"]
        read_only_fields = ["id", "friend_ids"]


class UserGroupSerializer(serializers.ModelSerializer):
    administrator_ids = serializers.SerializerMethodField("get_administrator_ids")
    member_ids = serializers.SerializerMethodField("get_member_ids")

    class Meta:
        model = UserGroup
        fields = ["id", "name", "description", "administrator_ids", "member_ids"]
        read_only_fields = ["id", "administrator_ids", "member_ids"]

    def get_administrator_ids(self, obj):
        return [admin.id for admin in obj.administrators.all()]

    def get_member_ids(self, obj):
        return [member.id for member in obj.members.all()]


class UserGroupMiniSerializer(serializers.ModelSerializer):
    group_detail_url = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = ["id", "name", "group_detail_url"]

    def get_group_detail_url(self, obj):
        return reverse("users:group_detail", kwargs={"pk": obj.pk})


class FriendInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendInvitation
        fields = [
            "id",
            "sender",
            "receiver",
            "date_sent",
        ]


class GroupInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendInvitation
        fields = ["id", "sender", "receiver", "group", "date_sent"]


class InvitationResponseSerializer(serializers.Serializer):
    response = serializers.ChoiceField(
        choices=(("accept", "Accept invitation"), ("decline", "Decline invitation"))
    )
