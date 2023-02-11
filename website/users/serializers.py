from rest_framework import serializers
from django.urls import reverse

from .models import CustomUser, UserGroup, FriendInvitation, GroupInvitation

# include nested models or not? (friends for user, members and admins for a group)


class UserProfileSerializer(serializers.ModelSerializer):
    # only for displaying user's public information
    # add fields with nested serializers/list of ids for friends and groups
    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_picture"]


class UserMiniSerializer(serializers.ModelSerializer):
    # Serializer to use in lists
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_url"]

    def get_profile_url(self, obj):
        return reverse("users:user_profile", kwargs={"pk": obj.pk})


class UserOwnProfileSerializer(serializers.ModelSerializer):
    # own profile shows both public and private fields
    # Also for modifying own profile
    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_picture", "email", "is_active"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup


class FriendsInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendInvitation
