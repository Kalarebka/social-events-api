from rest_framework.views import APIView

from events.models import Event, Location
from .models import CustomUser


class UserDetailView(APIView):
    def get(self, request, pk):
        # user profile information
        pass

    def patch(self, request, pk):
        # Modify user information (only the user's own own data)
        pass

    def delete(self, request, pk):
        # delete user's account
        pass


class UserListView(APIView):
    def get(self, request):
        # list of all users (some option for users to not show up in public list?)
        pass

    def post(self, request):
        # register a new user
        pass


class FriendsListView(APIView):
    def get(self, request):
        # the user's friend list
        pass