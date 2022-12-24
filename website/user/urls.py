from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path("", views.UserListView.as_view()),
    path("/<int:pk>", views.UserDetailView.as_view()),
    path("friends/", views.FriendsListView.as_view())
]
