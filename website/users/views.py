from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.http import Http400
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FriendInvitation, GroupInvitation, UserGroup
from .permissions import (
    InvitationsPermission,
    OwnProfileOrReadOnly,
    UserGroupPermission,
)
from .serializers import (
    FriendInvitationSerializer,
    GroupInvitationSerializer,
    InvitationResponseSerializer,
    UserGroupMiniSerializer,
    UserGroupSerializer,
    UserMiniSerializer,
    UserOwnProfileSerializer,
    UserProfileSerializer,
)


class UserListView(ListAPIView):
    """GET: Retrieve a list of active user profiles.
    Query parameters:
    - minimal: bool, default: False; if True, use mini serializer (id, username, link to profile), otherwise - return full profiles
    - ids: list of integers - optional - will return users with the specified ids (format: "/users?ids=1,2,3,4)
    """

    def get_serializer_class(self):
        if self.request.query_params.get("minimal", False):
            return UserMiniSerializer
        return UserProfileSerializer

    def get_queryset(self):
        ids = self.request.query_params.get("ids", None)
        if not ids:
            return get_user_model().objects.all()
        id_list = [int(id) for id in ids.split(",")]
        return get_user_model().objects.filter(pk__in=id_list)


class UserProfileView(RetrieveUpdateAPIView):
    """
    GET: Retrieve a single user's profile by user id.
    For the currently logged in user's own profile, uses separate serializer that also returns private information.
    PUT/PATCH: User can update own profile.
    """

    queryset = get_user_model().objects.all()
    permission_classes = [OwnProfileOrReadOnly]

    def get_serializer_class(self):
        if self.kwargs["pk"] == self.request.user.pk:
            return UserOwnProfileSerializer
        return UserProfileSerializer


class FriendDetailView(APIView):
    def post(self, request, friend_pk):
        """Send a friend invitation to user with friend_pk"""
        receiver = get_object_or_404(get_user_model(), pk=friend_pk)
        if receiver in request.user.friends.all():
            return Response(
                {"message": "user already on friends list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        invitation = FriendInvitation(sender=request.user, receiver=receiver)
        invitation.save()
        return Response(
            {"message": "invitation sent"},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, friend_pk):
        """Remove current user and friend from each other's friend lists"""
        user = request.user
        friend = get_object_or_404(get_user_model(), pk=friend_pk)
        if friend not in request.user.friends.all():
            return Response(
                {"message": "no such user on friend list"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.friends.remove(friend)
        return Response(
            {"message": f"User {friend.id} removed from friends"},
            status=status.HTTP_200_OK,
        )


class GroupsListView(ListCreateAPIView):
    """
    GET: Retrieve current user's groups
         Query parameters:
            - minimal: bool, default: False; if True, use mini serializer (id, group name, link to group detail)
    POST - create a group
    """

    def get_serializer_class(self):
        if self.request.query_params.get("minimal", False):
            return UserGroupMiniSerializer
        return UserGroupSerializer

    def get_queryset(self):
        # list groups as member - to be an admin of a group, user has to also be a member
        return self.request.user.groups_as_member.filter(deleted=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_kwargs = {
            "administrators": [request.user],
            "members": [request.user],
        }
        group = serializer.save(**group_kwargs)
        return Response({"id": group.id}, status=status.HTTP_201_CREATED)


class GroupsDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET - group details (group members only)
    PUT/PATCH - edit group details (admin only)
    DELETE - delete group (== set deleted=True, leave in db) (admin only)
    """

    queryset = UserGroup.objects.filter(deleted=False)
    serializer_class = UserGroupSerializer
    permission_classes = [
        UserGroupPermission,
    ]

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class GroupMembersDetailView(APIView):
    permission_classes = [UserGroupPermission]

    def post(self, request, group_pk, user_pk):
        """Send group invitation to user. Path parameters: group_pk, user_pk"""
        group = get_object_or_404(UserGroup, pk=group_pk)
        receiver = get_object_or_404(get_user_model(), pk=user_pk)
        if receiver in group.members.all():
            return Response(
                {"message": "user already a member of the group"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        invitation = GroupInvitation(
            sender=request.user, receiver=receiver, group=group
        )
        invitation.save()
        return Response(
            {"message": "invitation sent"},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, group_pk, user_pk):
        """Remove user from group"""
        group = get_object_or_404(UserGroup, pk=group_pk)
        user = get_object_or_404(get_user_model(), pk=user_pk)
        if user not in group.members.all():
            return Response(
                {"message": "user is not a member of the group"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GroupAdminsDetailView(APIView):
    permission_classes = [UserGroupPermission]

    def post(self, request, group_pk, user_pk):
        """Make another user an admin of the group"""
        group = get_object_or_404(UserGroup, pk=group_pk)
        user = get_object_or_404(get_user_model(), pk=user_pk)

        if user not in group.members.all():
            return Response(
                {"message": "user is not a member of the group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        group.administrators.add(user)
        group.save()
        return Response(
            {"message": "user added to group admins"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, group_pk, user_pk):
        """Take away user's admin status"""
        group = get_object_or_404(UserGroup, pk=group_pk)
        user = get_object_or_404(get_user_model(), pk=user_pk)

        if user not in group.administrators.all():
            return Response(
                {"message": "user is not an administrator of the group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # The only remaining admin cannot be removed
        if group.administrators.all().count() == 1:
            return Response(
                {
                    "message": "Last remaining admin of the group cannot be removed.\
                                Nominate another admin first or delete the group.",
                }
            )
        group.administrators.remove(user)
        group.save()
        return Response(
            {"message": "user removed from group admins"},
            status=status.HTTP_200_OK,
        )


class InvitationsListView(ListAPIView):
    """
    GET - list of invitations
    query parameters:
    - invite_type: friends/groups
    - category: sent/received (default: received)
    Sent - invitations sent by the user
    Received - current user's received invitations without response"""

    def get_queryset(self):
        user = self.request.user
        invite_type = self.request.query_params.get["invite_type"]
        if not invite_type:
            raise Http400
        queryset_dict = {
            "friends": FriendInvitation.objects.all(),
            "groups": GroupInvitation.objects.all(),
        }
        qs = queryset_dict[invite_type]

        category = self.request.query_params.get["category"]
        if category == "sent":
            return qs.filter(sender=user)
        return qs.filter(receiver=user, response_received=False)

    def get_serializer_class(self):
        # list() method in list mixin calls get_queryset first, so no need to check
        # again if invite_type was provided
        invite_type = self.request.query_params.get["invite_type"]
        serializer_dict = {
            "friends": FriendInvitationSerializer,
            "groups": GroupInvitationSerializer,
        }
        return serializer_dict[invite_type]


class AbstractInvitationDetailView(ABC, APIView):
    """Handle different types of invitations.
    GET - get single invitation details
    DELETE - delete the invitation (only in response not received)"""

    permission_classes = [InvitationsPermission]

    @abstractmethod
    def get_serializer_class(self):
        pass

    @abstractmethod
    def get_object(self, pk):
        pass

    def get(self, request, pk):
        """GET - Single invitation details"""
        invitation = self.get_object(pk)
        serializer = self.get_serializer_class(invitation)
        return Response(serializer.data)

    def delete(self, request, pk):
        """DELETE: cancel the invitation"""
        invitation = self.get_object(pk)

        if invitation.response_received:
            return Response(
                {"detail": "Response already received, invitation cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendInvitationDetailView(AbstractInvitationDetailView):
    def get_serializer_class(self):
        return FriendInvitationSerializer

    def get_object(self, pk):
        return get_object_or_404(FriendInvitation, pk=pk)


class GroupInvitationDetailView(AbstractInvitationDetailView):
    def get_serializer_class(self):
        return GroupInvitationSerializer

    def get_object(self, pk):
        return get_object_or_404(GroupInvitation, pk=pk)


class InvitationResponseView(APIView):
    """
    Receive responses to invitations
    """

    def get(self, request, pk):
        # Accepting by GET method for compatibility with invitation response links in email
        invitation_response = request.query_params.get("response", None)
        if invitation_response in ["accept", "decline"]:
            invitation = get_object_or_404(GroupInvitation, pk=pk)
            invitation.send_response(invitation_response)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"error": "Response must be one of the following: accept or decline"},
            status=status.HTTP_400_BAD_REQUEST,
        )
