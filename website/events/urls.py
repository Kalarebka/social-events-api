from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    EventInvitationDetailView,
    EventInvitationsListView,
    EventOrganiserDetailView,
    EventOrganisersListView,
    EventParticipantDetailView,
    EventParticipantsListView,
    EventViewSet,
    LocationDetailView,
    LocationsListView,
)

router = DefaultRouter()
router.register("", EventViewSet, basename="events")


urlpatterns = [
    path("", include(router.urls)),
    path("<int:event_pk>/participants/", EventParticipantsListView.as_view()),
    path(
        "<int:event_pk>/participants/<int:user_pk>",
        EventParticipantDetailView.as_view(),
    ),
    path("<int:event_pk>/organisers/", EventOrganisersListView.as_view()),
    path("<int:event_pk>/organisers/<int:user_pk>", EventOrganiserDetailView.as_view()),
    path("invitations/", EventInvitationsListView.as_view()),
    path(
        "invitations/<int:pk>", EventInvitationDetailView.as_view()
    ),  # POST response="accept"/"decline"
    path(
        "locations/", LocationsListView.as_view()
    ),  # list and post to user's saved locations
    path(
        "locations/<int:pk>", LocationDetailView.as_view()
    ),  # see details, update, delete user's locations
]
