from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView

from .models import CustomUser, UserGroup
from .serializers import UserProfileSerializer, GroupSerializer, InvitationSerializer


class UserListView(ListAPIView):
    # Retrieve a list of all active user profiles
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer


class CurrentUserProfileView(RetrieveUpdateDestroyAPIView):
    # GET - own profile
    # PUT - update own profile
    # DELETE - deactivate own profile (remains in the db, but not visible)
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    # How to get /<pk> view to resolve to request.user's id?
    # Separate Serializer, so the user can see and change more information (e.g. username, email)


class UserProfileView(RetrieveAPIView):
    # GET - user profile by id (only active users)
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer


class FriendsListView(ListAPIView):
    # GET - list of current user's friends
    # POST (user id in request data) - send friend invitation// ?? in detail view? post or patch?
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return user.friends.all()


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
