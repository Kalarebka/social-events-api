from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Event, Location


class EventView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            content = {"app status": "working"}
            return Response(content)
        # Get one event
        pass

    def post(self, request):
        # Create an event
        pass

    def put(self, request, pk):
        # Edit the event (organiser only)
        pass

    def delete(self, request, pk):
        # Organiser only
        pass


class EventUsersView(APIView):
    def get(self, request, pk):
        # get all users that will attend the event
        pass


class EventInviteView(APIView):
    def post(self, request):
        # a list of users (id's) to invite in POST data (can have 1 user)
        # send invitations to the users (separate function outside views)
        pass


# maybe this should be under user/locations??
class LocationListView(APIView):
    def get(self, request):
        # current user's saved locations
        pass

    def post(self, request):
        # add a location to user's saved locations
        pass


class LocationDetailView(APIView):
    def get(self, request):
        # one location info
        pass


class CalendarView(APIView):
    def get(self):
        pass
