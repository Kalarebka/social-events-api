from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EventViewSet,
    EventParticipantsView,
)


router = DefaultRouter()
router.register("events", EventViewSet, basename="event")


urlpatterns = [
    path("", include(router.urls)),
    path("<int:pk>/participants/", EventParticipantsView.as_view()),
]

# urlpatterns = [
#     path("", EventView.as_view()),
#     path("<int:pk>/", EventView.as_view()),
#
#     path("<int:pk>/invite/", EventInviteView.as_view()),
#     path("calendar/", CalendarView.as_view()),
#     path("location/", LocationListView.as_view()),
#     path("location/<int:pk>", LocationDetailView.as_view()),
# ]
