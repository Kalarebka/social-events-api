from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from invitations.tasks import send_invitation_email
from invitations.views import (
    AbstractInvitationDetailView,
    AbstractInvitationResponseView,
    AbstractEmailInvitationResponseView,
    AbstractInvitationListView,
)

from .models import Event, EventInvitation
from .permissions import EventPermission
from .serializers import (
    EventCreateUpdateSerializer,
    EventInvitationSerializer,
    EventRetrieveSerializer,
    LocationSerializer,
    RecurringEventScheduleSerializer,
)


class EventViewSet(ModelViewSet):
    permission_classes = [EventPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "status": ["exact"],
        "event_type": ["exact"],
    }

    def get_queryset(self):
        # Only events in which the user is a participant (including not confirmed)
        user = self.request.user
        return user.events

    def get_serializer_class(self):
        if self.request.method == "GET":
            return EventRetrieveSerializer
        return EventCreateUpdateSerializer


class EventParticipantDetailView(APIView):
    permission_classes = [EventPermission]

    def post(self, request, event_pk, user_pk):
        """Send event invitation to user. Path parameters: event_pk, user_pk."""
        event = get_object_or_404(Event, pk=event_pk)
        self.check_object_permissions(request, event)
        recipient = get_object_or_404(get_user_model(), pk=user_pk)
        if recipient in event.participants.all():
            return Response(
                {"message": "user already invited to the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Create invitation
        invitation = EventInvitation(
            sender=request.user, recipient=recipient, event=event
        )
        invitation.save()

        # Set celery task to send invitation email
        send_invitation_email.delay(invitation)

        return Response(
            {"message": "invitation sent"},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, event_pk, user_pk):
        "Remove user from event participants. Path parameters: event_pk, user_pk."
        user_to_remove = get_object_or_404(get_user_model(), pk=user_pk)
        event = get_object_or_404(Event, pk=event_pk)
        self.check_object_permissions(request, event)
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
    permission_classes = [EventPermission]

    def post(self, request, event_pk, user_pk):
        """Make another user an organiser of the event"""
        event = get_object_or_404(Event, pk=event_pk)
        user = get_object_or_404(get_user_model(), pk=user_pk)
        self.check_object_permissions(request, event)

        if user not in event.organisers.all():
            return Response(
                {"message": "The user is not an organiser of the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event.organisers.add(user)
        return Response(
            {"message": "user added to event organisers"},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, event_pk, user_pk):
        """Take away user's organiser status"""
        event = get_object_or_404(Event, pk=event_pk)
        user = get_object_or_404(get_user_model(), pk=user_pk)
        self.check_object_permissions(request, event)

        if user not in event.organisers.all():
            return Response(
                {"message": "user is not an organiser of the event"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # The only remaining organiser cannot be removed
        if event.organisers.all().count() == 1:
            return Response(
                {
                    "message": "Last remaining organiser of the event cannot be removed.\
                                Nominate another organiser first or cancel the event.",
                }
            )
        event.organisers.remove(user)
        event.save()
        return Response(
            {"message": "user removed from event organisers"},
            status=status.HTTP_200_OK,
        )


class EventInvitationsListView(AbstractInvitationListView):
    """
    GET - list of event invitations
    query parameter:
    - category:
      -> sent - invitations sent by the user
      -> received (default) - current user's received invitations without response
    """

    serializer_class = EventInvitationSerializer

    def get_invitation_model(self):
        return EventInvitation


class EventInvitationDetailView(AbstractInvitationDetailView):
    serializer_class = EventInvitationSerializer

    def get_invitation_model(self):
        return EventInvitation


class EventInvitationResponseView(AbstractInvitationResponseView):
    def get_invitation_model(self):
        return EventInvitation


class EventInvitationEmailResponseView(AbstractEmailInvitationResponseView):
    def get_invitation_model(self):
        return EventInvitation


class LocationsListView(ListCreateAPIView):
    """GET: retrieve current user's saved locations
    POST: create a location, query parameter: save: bool, default=False
    If True, will add the location to the user's saved_locations"""

    serializer_class = LocationSerializer

    def get_queryset(self):
        return self.request.user.saved_locations.all()


class LocationDetailView(RetrieveUpdateDestroyAPIView):  # TODO
    """
    Location detail view

    All users can see location details, the user who saved the location can edit and delete it.
    POST - copy the location to own saved locations
    """

    # TODO permission that checks if location.saved_by == request.user for edit and delete
    permission_classes = []
    serializer_class = LocationSerializer


class RecurrenceScheduleListView(CreateAPIView):  # TODO
    """
    Create a schedule for recurring events

    When a schedule is created, event occurrences are created based on the base event and schedule
    """

    serializer_class = RecurringEventScheduleSerializer


class RecurrenceScheduleDetailView(RetrieveDestroyAPIView):  # TODO
    """
    Single recurrence schedule

    GET - retrieve schedule details and list of scheduled events
    DELETE - cancel all events except base event

    """

    pass


class CalendarView(APIView):  # TODO
    """Get user's events

    - filtered by day/month/year
    - minimal or full info about the event
    - confirmed or invited (or both??? in nested lists)
    """

    def get(self):
        pass
