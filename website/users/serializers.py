from rest_framework.serializers import ModelSerializer

from .models import CustomUser, UserGroup

# include nested models or not? (friends for user, members and admins for a group)


class UserProfileSerializer(ModelSerializer):
    # only for displaying user's public information
    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_picture"]


class UserMiniSerializer(ModelSerializer):
    # Serializer to use in lists
    # profile_url = url to the user profile view
    class Meta:
        model = CustomUser
        fields = ["id", "username", "profile_url"]


class UserOwnProfileSerializer(ModelSerializer):
    # own profile shows both public and private fields
    # Also for modifying own profile
    class Meta:
        model = CustomUser
        fields = []


class GroupSerializer(ModelSerializer):
    class Meta:
        model = UserGroup


class InvitationSerializer(ModelSerializer):
    # make separate serializers for GroupInvitation and FriendsInvitation
    pass
