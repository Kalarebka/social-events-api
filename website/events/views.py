from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Event
from .permissions import EventPermission
from .serializers import (
    EventCreateUpdateSerializer,
    EventRetrieveSerializer,
    LocationSerializer,
)

User = get_user_model()


class EventViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, EventPermission]
    queryset = Event.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return EventRetrieveSerializer
        return EventCreateUpdateSerializer


class EventParticipantsListView(APIView):
    # instead of get --> GET users:user_list with a list of ids
    # move post to detail view with user_pk as path parameter
    def get(self, request, pk):
        # get all event participants
        pass

    def post(self, request, pk):
        # send event invitations to users
        pass


class EventParticipantDetailView(APIView):
    permission_classes = []  # TODO /event organisers

    def post(self, event_pk, request, user_pk):
        """Send an event invitation to user"""
        user_to_invite = get_object_or_404(User, pk=user_pk)
        group = get_object_or_404(Event, pk=event_pk)
        # Check if user is already invited
        # If yes, 304 not modified
        # create event invitation (helper function ~ invite_to_event(user, event))

    def delete(self, event_pk, request, user_pk):
        "Remove user from event participants and invited users"
        user_to_remove = get_object_or_404(User, pk=user_pk)
        group = get_object_or_404(Event, pk=event_pk)
        # Check if user is in the group
        # If not, return 304 not modified
        # group.participants.remove(user_to_remove)
        # group.invited_users.remove(user_to_remove)


class EventOrganisersListView(APIView):
    pass


class EventOrganiserDetailView(APIView):
    pass


class EventInvitationsListView(APIView):
    pass


class EventInvitationDetailView(APIView):
    pass


class LocationsListView(ListCreateAPIView):
    """GET: retrieve current user's saved locations
    POST: create a location, query parameter: save: bool, default=False
    If True, will add the location to the user's saved_locations"""

    serializer_class = LocationSerializer

    def get_queryset(self):
        return self.request.user.saved_locations.all()


class LocationDetailView(RetrieveAPIView):
    def get(self, request):
        # one location info
        pass


class CalendarView(APIView):
    def get(self):
        pass
