from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView

from .models import CustomUser, UserGroup
from .permissions import OwnProfileOrReadOnly
from .serializers import (
    UserProfileSerializer,
    UserMiniSerializer,
    UserOwnProfileSerializer,
    GroupSerializer,
    InvitationSerializer,
)


class UserListView(ListAPIView):
    """GET: Retrieve a list of active user profiles.
    Query parameters:
    - minimal: bool, default: False; if True, use mini serializer (id, username, link to profile), otherwise - return full profiles
    - ids: list of integers - optional - will return users from the list
    """

    def get_serializer_class(self):
        if self.request.query_params.get("minimal", False):
            return UserMiniSerializer
        return UserProfileSerializer

    def get_queryset(self):
        if self.request.query_params.get("friends", False):
            return self.request.user.friends.all()
        return CustomUser.objects.all()


class UserProfileView(RetrieveUpdateAPIView):
    """GET: Retrieve a single user's profile by user id.
    For the currently logged in user's own profile, use separate serializer that also returns private information.
    PUT/PATCH: User can update own profile."""

    queryset = CustomUser.objects.all()
    permission_classes = [OwnProfileOrReadOnly]

    def get_serializer_class(self):
        if self.args["pk"] == self.request.user.pk:
            return UserOwnProfileSerializer
        return UserProfileSerializer


class FriendsListView(ListAPIView):
    """GET: Retrieve a list of current user's friends
    Query parameters:
    - minimal: bool, default: False; if True, use mini serializer (id, username, link to profile), otherwise - return full profiles
    POST: {"id": <id of the user to invite>} - send friend invitation
    """

    def get_serializer_class(self):
        if self.request.query_params.get("minimal", False):
            return UserMiniSerializer
        return UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return user.friends.filter(active=True)


class FriendDetailView(APIView):
    def delete(self, request, pk):
        # remove user from current user's friends
        pass


class GroupsListView(ListCreateAPIView):
    # GET - list all available groups
    # Missing an endpoint to show groups current user belongs to, not decided where yet
    # POST - create a group (user set as admin and member)
    queryset = (
        UserGroup.objects.all()
    )  # could have some filter, e.g. for private groups that won't show up
    serializer = GroupSerializer


class GroupsDetailView(RetrieveUpdateDestroyAPIView):
    # GET - group details
    # PUT/PATCH - edit group details (admin only) (DestroyMixin provides both put and patch)
    # DELETE - delete group (admin only)
    queryset = UserGroup.objects.all()
    serializer = GroupSerializer
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
        # remove user from group
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


class InvitationsListView(APIView):
    # very mysterious
    # show all user's unconfirmed invitations
    # can ListAPIView use two models (group and friends invitation)? probably not.
    # it would be perfect if it could also get event invitations,
    # but what if they're in different app? no idea.
    pass


class InvitationDetailView(APIView):
    def patch(self, request, pk):
        # some magic to confirm the invitation and modify necessary objects <- in invitations method
        # should call the invitation's confirm() method
        pass

    def delete(self, request, pk):
        # just delete or do something to show it was declined?
        pass
