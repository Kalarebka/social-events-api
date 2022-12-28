from django.urls import path

from .views import EventListView, EventDetailView, EventUsersView, EventInviteView, CalendarView, LocationListView, LocationDetailView

app_name = "event"
urlpatterns = [
    path("", EventListView.as_view()),
    path("<int:pk>/", EventDetailView.as_view()),
    path("<int:pk>/userlist/", EventUsersView.as_view()),
    path("<int:pk>/invite/", EventInviteView.as_view()),
    path("calendar/", CalendarView.as_view()),
    path("location/", LocationListView.as_view()),
    path("location/<int:pk>", LocationDetailView.as_view()),
]
