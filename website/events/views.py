from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.views import AbstractInvitationDetailView
from .models import Event, EventInvitation
from .permissions import EventPermission
from .serializers import (
    EventCreateUpdateSerializer,
    EventRetrieveSerializer,
    LocationSerializer,
    RecurringEventScheduleSerializer,
    EventInvitationSerializer,
)

User = get_user_model()


class EventViewSet(ModelViewSet):
    permission_classes = [EventPermission]

    def get_queryset(self):
        # todo filter by user.request in participants
        # filter by query parameters: status
        return Event.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EventRetrieveSerializer
        return EventCreateUpdateSerializer


class EventParticipantDetailView(APIView):
    permission_classes = [EventPermission]

    def post(self, request, event_pk, user_pk):
        """Send event invitation to user. Path parameters: event_pk, user_pk"""
        event = get_object_or_404(Event, pk=event_pk)
        receiver = get_object_or_404(get_user_model(), pk=user_pk)
        if receiver in event.participants.all():
            return Response(
                {"message": "user already invited to the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        invitation = EventInvitation(
            sender=request.user, receiver=receiver, event=event
        )
        invitation.save()
        return Response(
            {"message": "invitation sent"},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, event_pk, user_pk):
        "Remove user from event participants"
        user_to_remove = get_object_or_404(User, pk=user_pk)
        event = get_object_or_404(Event, pk=event_pk)
        if user_to_remove in event.participants.all():
            return Response(
                {"message": "user is not a member of the group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event.participants.remove(user_to_remove)
        # User can't be an organiser if he's not a participant in the event
        event.organisers.remove(user_to_remove)

        return Response(
            {"message": "user removed from the event"},
            status=status.HTTP_200_OK,
        )


class EventOrganiserDetailView(APIView):
    pass


class EventInvitationsListView(APIView):
    pass


class EventInvitationDetailView(AbstractInvitationDetailView):
    def get_serializer(self, qs):
        return EventInvitationSerializer(qs)

    def get_object(self, pk):
        return get_object_or_404(EventInvitation, pk=pk)


class LocationsListView(ListCreateAPIView):
    """GET: retrieve current user's saved locations
    POST: create a location, query parameter: save: bool, default=False
    If True, will add the location to the user's saved_locations"""

    serializer_class = LocationSerializer

    def get_queryset(self):
        return self.request.user.saved_locations.all()


class LocationDetailView(RetrieveUpdateDestroyAPIView):
    """
    User's saved locations view
    """

    # permission that checks if location.saved_by == request.user
    permission_classes = []
    serializer_class = LocationSerializer


class RecurrenceScheduleListView(CreateAPIView):
    """Create schedules for recurring events"""

    serializer_class = RecurringEventScheduleSerializer


class CalendarView(APIView):
    # Get events confirmed by the user, filtered by day/month/year
    # with basic data about the event and links to event details
    def get(self):
        pass
