from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CalendarView,
    EventInvitationDetailView,
    EventInvitationEmailResponseView,
    EventInvitationResponseView,
    EventInvitationsListView,
    EventOrganiserDetailView,
    EventParticipantDetailView,
    EventViewSet,
    LocationDetailView,
    LocationsListView,
    RecurrenceScheduleDetailView,
    RecurrenceScheduleListView,
)

router = DefaultRouter()
router.register("", EventViewSet, basename="events")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:event_pk>/participants/<int:user_pk>",
        EventParticipantDetailView.as_view(),
        name="participant_detail",
    ),
    path(
        "<int:event_pk>/organisers/<int:user_pk>",
        EventOrganiserDetailView.as_view(),
        name="organiser_detail",
    ),
    path("invitations/", EventInvitationsListView.as_view(), name="invitation_list"),
    path(
        "invitations/<int:pk>",
        EventInvitationDetailView.as_view(),
        name="invitation_detail",
    ),
    path(
        "invitations/<int:pk>/email-response/",
        EventInvitationEmailResponseView.as_view(),
        name="invitation_email_response",
    ),
    path(
        "invitations/<int:pk>/response/",
        EventInvitationResponseView.as_view(),
        name="invitation_response",
    ),
    path("locations/", LocationsListView.as_view(), name="location_list"),
    path("locations/<int:pk>", LocationDetailView.as_view(), name="location_detail"),
    path("schedules/", RecurrenceScheduleListView.as_view(), name="schedule_list"),
    path(
        "schedules/<int:pk>",
        RecurrenceScheduleDetailView.as_view(),
        name="schedule_detail",
    ),
    path("calendar/", CalendarView.as_view(), name="calendar"),
]
