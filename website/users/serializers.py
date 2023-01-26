from rest_framework.serializers import ModelSerializer

from .models import CustomUser, UserGroup

# include nested models or not? (friends for user, members and admins for a group)


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "profile_picture")
        read_only_fields = ("id", "username")


class GroupSerializer(ModelSerializer):
    class Meta:
        model = UserGroup


class InvitationSerializer(ModelSerializer):
    # make separate serializers for GroupInvitation and FriendsInvitation
    pass
