from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EventViewSet,
    EventParticipantsListView,
    EventParticipantDetailView,
    EventOrganisersListView,
    EventOrganiserDetailView,
    EventInvitationsListView,
    EventInvitationDetailView,
    LocationsListView,
    LocationDetailView,
)


router = DefaultRouter()
router.register("events", EventViewSet, basename="event")


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
    ),  # Update - accept invitation, delete - decline
    path(
        "locations/", LocationsListView.as_view()
    ),  # list and post to user's saved locations
    path(
        "locations/<int:pk>", LocationDetailView.as_view()
    ),  # see details, update, delete user's locations
]
