# event.urls

from django.urls import path

from . import views

app_name = "event"
urlpatterns = [
    path("", views.EventListView.as_view()),
    path("<int:pk>/", views.EventDetailView.as_view()),
    path("<int:pk>/userlist/", views.EventUsersView.as_view()),
    path("<int:pk>/invite/", views.EventInviteView.as_view()),
    path("calendar/", views.CalendarView.as_view()),
    path("location/", views.LocationListView.as_view()),
    path("location/<int:pk>", views.LocationDetailView.as_view()),
]
