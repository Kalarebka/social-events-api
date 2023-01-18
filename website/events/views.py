from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Event, Location
from .permissions import EventPermissions
from .serializers import EventSerializer


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, EventPermissions]
    queryset = Event.objects.all()

    def get_queryset(self):
        # ? but user should also be able to see events he's invited to
        return self.queryset.exclude(event_access="invitation")


class EventParticipantsView(APIView):
    def get(self, request, pk):
        # get all event participants
        pass

    def post(self, request, pk):
        # add current user to event participants
        # user can join public events and event of groups he's a part of without invitation
        pass


class EventInviteView(APIView):
    def post(self, request):
        # a list of users (id's) to invite in POST data (can have 1 user)
        # send invitations to the users (separate function outside views)
        pass


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
