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
    path(
        "<int:pk>/participants/", EventParticipantsListView.as_view()
    ),  # list of participants, add participants (invite): post user/group/list of users/all friends
    path(
        "<int:pk>/participants/<int:user_pk>", EventParticipantDetailView.as_view()
    ),  # remove participant
    path(
        "<int:pk>/participants/", EventOrganisersListView.as_view()
    ),  # list organisers, post - add an organiser
    path(
        "<int:pk>/participants/<int:user_pk>", EventOrganiserDetailView.as_view()
    ),  # remove organiser
    path("invitations/", EventInvitationsListView.as_view()),  # all user's invitations
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
