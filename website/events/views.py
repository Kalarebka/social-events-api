from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Event, Location
from .permissions import EventPermission
from .serializers import EventRetrieveSerializer, EventCreateUpdateSerializer


class EventViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, EventPermission]
    queryset = Event.objects.all()

    def get_queryset(self):
        return self.queryset  # Override with only events the user should be able to see

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return EventRetrieveSerializer
        return EventCreateUpdateSerializer


class EventParticipantsListView(APIView):
    def get(self, request, pk):
        # get all event participants
        pass

    def post(self, request, pk):
        # add current user to event participants
        # user can join public events and event of groups he's a part of without invitation
        pass


class EventParticipantDetailView(APIView):
    pass


class EventOrganisersListView(APIView):
    pass


class EventOrganiserDetailView(APIView):
    pass


class EventInvitationsListView(APIView):
    pass


class EventInvitationDetailView(APIView):
    pass


class LocationListView(APIView):
    def get(self, request):
        # current user's saved locations
        pass

    def post(self, request):
        # create a location and return it's id
        # parameter: save: bool - if True, add the location to user's saved locations
        pass


class LocationsListView(APIView):
    pass


class LocationDetailView(APIView):
    def get(self, request):
        # one location info
        pass


class CalendarView(APIView):
    def get(self):
        pass
