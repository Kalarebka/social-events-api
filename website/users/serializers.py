from django.urls import reverse
from rest_framework import serializers

from .models import CustomUser, FriendInvitation, GroupInvitation, UserGroup


class UserProfileSerializer(serializers.ModelSerializer):
    """Public user profile information, for retrieve only views"""

    friend_ids = serializers.SerializerMethodField("get_friend_ids")
    group_ids = serializers.SerializerMethodField("get_group_ids")

    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_picture", "friend_ids", "group_ids"]

    def get_friend_ids(self, obj):
        return [friend.id for friend in obj.friends.all()]

    def get_group_ids(self, obj):
        return [group.id for group in obj.groups_as_member.all()]


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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup


class FriendInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendInvitation
