from django.contrib.auth import get_user_model
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
    IsGroupAdmin,
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
    """GET: Retrieve a single user's profile by user id.
    For the currently logged in user's own profile, uses separate serializer that also returns private information.
    PUT/PATCH: User can update own profile."""

    queryset = get_user_model().objects.all()
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
        friend = get_object_or_404(User, pk=friend_pk)
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
            return get_user_model().objects.all()
        id_list = [int(id) for id in ids.split(",")]
        return get_user_model().objects.filter(pk__in=id_list)

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
    permission_classes = [IsGroupAdmin]

    def post(self, request, group_pk, user_pk):
        """Make another user an admin of the group"""
        group = get_object_or_404(UserGroup, pk=group_pk)
        user = get_object_or_404(get_user_model(), pk=user_pk)

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
        user = get_object_or_404(get_user_model(), pk=user_pk)
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
    - invite_type: friends/groups
    - category: sent/received (default: received)
    Sent - invitations sent by the user
    Received - current user's received invitations without response"""

    def get_serializer_class(self):
        invite_type = self.request.query_params.get["invite_type"]
        if invite_type == "friends":
            return FriendInvitationSerializer
        elif invite_type == "groups":
            return GroupInvitationSerializer
        else:
            pass  # TODO has to raise error if no invite_type parameter

    def get_queryset(self):
        user = self.request.user
        invite_type = self.request.query_params.get["invite_type"]
        if invite_type == "friends":
            qs = FriendInvitation.objects.all()  # dict!
        elif invite_type == "groups":
            qs = GroupInvitation.objects.all()
        else:
            pass  # TODO has to raise error if no invite_type parameter

        category = self.request.query_params.get["category"]
        if category == "sent":
            return qs.filter(sender=user)
        return qs.filter(receiver=user, response_received=False)


# class FriendInvitationDetailView(APIView):
#     permission_classes = [InvitationsPermission]

#     def get(self, request, pk):
#         """GET - Single invitation details"""
#         invitation = FriendInvitation.objects.get(pk=pk)
#         serializer = FriendInvitationSerializer(invitation)
#         return Response(serializer.data)

#     def post(self, request, pk):
#         """POST - send response to the invitation
#         response: accept or decline"""
#         serializer = InvitationResponseSerializer(data=request.data)
#         if serializer.is_valid():
#             invitation = get_object_or_404(FriendInvitation, pk=pk)
#             invitation.send_response(serializer.data["response"])
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {"error": "Response must be one of the following: accept or decline"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     def delete(self, request, pk):
#         """DELETE: cancel the invitation (only before it receives a response)"""
#         invitation = get_object_or_404(FriendInvitation, pk=pk)

#         if invitation.response_received:
#             return Response(
#                 {"detail": "Response already received, invitation cannot be deleted."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         invitation.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class GroupInvitationDetailView(APIView):
#     permission_classes = [InvitationsPermission]

#     def get(self, request, pk):
#         """GET - Single invitation details"""
#         invitation = GroupInvitation.objects.get(pk=pk)
#         serializer = GroupInvitationSerializer(invitation)
#         return Response(serializer.data)

#     def post(self, request, pk):
#         """POST - send response to the invitation
#         response: accept or decline"""
#         serializer = InvitationResponseSerializer(data=request.data)
#         if serializer.is_valid():
#             invitation = get_object_or_404(GroupInvitation, pk=pk)
#             invitation.send_response(serializer.data["response"])
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {"error": "Response must be one of the following: accept or decline"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#     def delete(self, request, pk):
#         """DELETE: cancel the invitation (only before it receives a response)"""
#         invitation = get_object_or_404(GroupInvitation, pk=pk)

#         if invitation.response_received:
#             return Response(
#                 {"detail": "Response already received, invitation cannot be deleted."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         invitation.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationDetailView(APIView):
    # Merge friends and groups invitations
    permission_classes = [InvitationsPermission]

    def get(self, request, pk):
        """GET - Single invitation details"""
        invitation = GroupInvitation.objects.get(pk=pk)
        serializer = GroupInvitationSerializer(invitation)
        return Response(serializer.data)

    def post(self, request, pk):
        """POST - send response to the invitation
        response: accept or decline"""
        serializer = InvitationResponseSerializer(data=request.data)
        if serializer.is_valid():
            invitation = get_object_or_404(GroupInvitation, pk=pk)
            invitation.send_response(serializer.data["response"])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Response must be one of the following: accept or decline"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        """DELETE: cancel the invitation (only before it receives a response)"""
        invitation = get_object_or_404(GroupInvitation, pk=pk)

        if invitation.response_received:
            return Response(
                {"detail": "Response already received, invitation cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
