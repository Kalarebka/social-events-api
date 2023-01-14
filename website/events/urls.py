from django.urls import path

from .views import (
    EventView,
    EventUsersView,
    EventInviteView,
    CalendarView,
    LocationListView,
    LocationDetailView,
)

app_name = "events"
urlpatterns = [
    path("", EventView.as_view()),
    path("<int:pk>/", EventView.as_view()),
    path("<int:pk>/userlist/", EventUsersView.as_view()),
    path("<int:pk>/invite/", EventInviteView.as_view()),
    path("calendar/", CalendarView.as_view()),
    path("location/", LocationListView.as_view()),
    path("location/<int:pk>", LocationDetailView.as_view()),
]
