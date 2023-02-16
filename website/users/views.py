from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, UserGroup, FriendInvitation, GroupInvitation
from .permissions import OwnProfileOrReadOnly, UserGroupPermission, IsGroupAdmin
from .serializers import (
    UserProfileSerializer,
    UserMiniSerializer,
    UserOwnProfileSerializer,
    UserGroupSerializer,
    UserGroupMiniSerializer,
    FriendInvitationSerializer,
    GroupInvitationSerializer,
    InvitationResponseSerializer,
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
            return CustomUser.objects.all()
        id_list = [int(id) for id in ids.split(",")]
        return CustomUser.objects.filter(pk__in=id_list)


class UserProfileView(RetrieveUpdateAPIView):
    """GET: Retrieve a single user's profile by user id.
    For the currently logged in user's own profile, uses separate serializer that also returns private information.
    PUT/PATCH: User can update own profile."""

    queryset = CustomUser.objects.all()
    permission_classes = [OwnProfileOrReadOnly]

    def get_serializer_class(self):
        if self.kwargs["pk"] == self.request.user.pk:
            return UserOwnProfileSerializer
        return UserProfileSerializer


# not necessary? can get the same info by getting a user profile and requesting user list with the ids
class FriendsListView(ListCreateAPIView):
    """GET: Retrieve a list of current user's friends
    Query parameters:
    - minimal: bool, default: False; if True, use mini serializer (id, username, link to profile), otherwise - return full profiles
    """

    def get_serializer_class(self):
        if self.request.query_params.get("minimal", False):
            return UserMiniSerializer
        return UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return user.friends.all()


class FriendDetailView(APIView):
    def post(self, request, friend_pk):
        """Send a friend invitation to user with friend_pk"""
        receiver = get_object_or_404(CustomUser, pk=friend_pk)
        if receiver in request.user.friends.all():
            return Response(
                {"message": "user already on friends list"},
                status=status.HTTP_304_NOT_MODIFIED,
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
        friend = get_object_or_404(CustomUser, pk=friend_pk)
        if friend not in request.user.friends.all():
            return Response(
                {"message": "no such user on friend list"},
                status=status.HTTP_304_NOT_MODIFIED,
            )
        user.friends.remove(friend)
        return Response(
            {"message": f"User {friend.id} removed from friends"},
            status=status.HTTP_200_OK,
        )


class GroupsListView(ListCreateAPIView):
    """GET: Retrieve current user's groups
    Query parameters:
    - minimal: bool, default: False; if True, use mini serializer (id, group name, link to group detail)
    POST - create a group
    """

    serializer = UserGroupSerializer

    def get_serializer_class(self):
        if self.request.query_params.get("minimal", False):
            return UserGroupMiniSerializer
        return UserGroupSerializer

    def get_queryset(self):
        ids = self.request.query_params.get("ids", None)
        if not ids:
            return CustomUser.objects.all()
        id_list = [int(id) for id in ids.split(",")]
        return CustomUser.objects.filter(pk__in=id_list)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save(commit=False)
        group.administrators.add(request.user)
        group.members.add(request.user)
        group.save()
        return Response({"id": group.id}, status=status.HTTP_201_CREATED)


class GroupsDetailView(RetrieveUpdateDestroyAPIView):
    """GET - group details (group members only)
    PUT/PATCH - edit group details (admin only)
    DELETE - delete group (admin only)"""

    queryset = UserGroup.objects.all()
    serializer = UserGroupSerializer
    permission_classes = [
        UserGroupPermission,
    ]


class GroupMembersDetailView(APIView):
    permission_classes = [IsGroupAdmin]

    def post(self, request, group_pk, user_pk):
        """Send group invitation to user. Path parameters: group_pk, user_pk"""
        group = get_object_or_404(UserGroup, pk=group_pk)
        receiver = get_object_or_404(CustomUser, pk=user_pk)
        if receiver in group.members.all():
            return Response(
                {"message": "user already a member of the group"},
                status=status.HTTP_304_NOT_MODIFIED,
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
        user = get_object_or_404(CustomUser, pk=user_pk)
        if user not in group.members.all():
            return Response(
                {"message": "user is not a member of the group"},
                status=status.HTTP_304_NOT_MODIFIED,
            )


class GroupAdminsDetailView(APIView):
    permission_classes = [IsGroupAdmin]

    def post(self, request, group_pk, user_pk):
        """Make another user an admin of the group"""
        group = get_object_or_404(UserGroup, pk=group_pk)
        user = get_object_or_404(CustomUser, pk=user_pk)

        if user not in group.members.all():
            return Response(
                {"message": "user is not a member of the group"},
                status=status.HTTP_304_NOT_MODIFIED,
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
        user = get_object_or_404(CustomUser, pk=user_pk)
        if user not in group.administrators.all():
            return Response(
                {"message": "user is not an administrator of the group"},
                status=status.HTTP_304_NOT_MODIFIED,
            )
        group.administrators.remove(user)
        group.save()
        return Response(
            {"message": "user removed from group admins"},
            status=status.HTTP_200_OK,
        )


class InvitationsListView(ListAPIView):
    """GET - list of invitations
    query parameters:
    - kind: friends/groups
    - category: sent/received (default: received)
    Sent - invitations sent by the user
    Received - current user's received invitations without response"""

    def get_serializer_class(self):
        invite_type = self.request.query_params.get["invite_type"]
        if invite_type == "friends":
            return FriendInvitationSerializer
        elif invite_type == "groups":
            return GroupInvitationSerializer

    serializer_class = FriendInvitationSerializer

    def get_queryset(self):
        user = self.request.user
        category = self.request.query_params.get["category"]
        if category == "sent":
            return FriendInvitation.objects.filter(sender=user)
        return FriendInvitation.objects.filter(receiver=user, response_received=False)


class FriendInvitationDetailView(APIView):
    def get(self, request, pk):
        """GET - Single invitation details"""
        invitation = FriendInvitation.objects.get(pk=pk)
        serializer = FriendInvitationSerializer(invitation)
        return Response(serializer.data)

    def post(self, request, pk):
        """POST - send response to the invitation
        response: accept or decline"""
        serializer = InvitationResponseSerializer(data=request.data)
        if serializer.is_valid():
            invitation = get_object_or_404(FriendInvitation, pk=pk)
            invitation.send_response(serializer.data["response"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Response must be one of the following: accept or decline"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GroupInvitationDetailView(APIView):
    def get(self, request, pk):
        """GET - Single invitation details"""
        invitation = FriendInvitation.objects.get(pk=pk)
        serializer = FriendInvitationSerializer(invitation)
        return Response(serializer.data)

    def post(self, request, pk):
        """POST - send response to the invitation
        response: accept or decline"""
        serializer = InvitationResponseSerializer(data=request.data)
        if serializer.is_valid():
            invitation = get_object_or_404(FriendInvitation, pk=pk)
            invitation.send_response(serializer.data["response"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Response must be one of the following: accept or decline"},
                status=status.HTTP_400_BAD_REQUEST,
            )
