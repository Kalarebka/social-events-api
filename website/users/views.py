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
from .permissions import OwnProfileOrReadOnly
from .serializers import (
    UserProfileSerializer,
    UserMiniSerializer,
    UserOwnProfileSerializer,
    UserGroupSerializer,
    UserGroupMiniSerializer,
    FriendInvitationSerializer,
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
    # GET - group details
    # PUT/PATCH - edit group details (admin only) (DestroyMixin provides both put and patch)
    # DELETE - delete group (admin only)
    queryset = UserGroup.objects.all()
    serializer = UserGroupSerializer
    permission_classes = []  # some permission where only admin can update and delete


class GroupMembersListView(APIView):
    def get(self, request, pk):
        # get the group's members list
        pass


class GroupMembersDetailView(APIView):
    # group admin only
    def post(self, request, pk, user_pk):
        # method: post or patch? user_pk in url or parameters?
        # add user to group (== send invitation)
        pass

    def delete(self, request, pk, user_pk):
        # remove user from group (admin can remove any member; user can remove self)
        pass


class GroupAdminsListView(APIView):
    def get(self, request, pk):
        # get the group's admins list
        pass


class GroupAdminsDetailView(APIView):
    # group admin only
    def post(self, request, pk, user_pk):
        # make another user an admin
        # does not require the other user's permission
        pass

    def delete(self, request, pk, user_pk):
        # remove user from admins
        # if there is one admin and tries to remove themself, send back an appropriate
        # response code and message that they should first set another admin from users
        # or if they're the only user to delete the group)
        pass


class FriendInvitationsListView(ListAPIView):
    """GET - list of invitations
    query parameter: category: sent/received (default: received)
    Sent - invitations sent by the user
    Received - current user's received invitations without response"""

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
