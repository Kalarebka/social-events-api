from django.urls import path

from .views import (
    UserListView,
    CurrentUserProfileView,
    UserProfileView,
    FriendsListView,
    FriendDetailView,
    GroupsListView,
    GroupsDetailView,
    GroupMembersListView,
    GroupMembersDetailView,
    GroupAdminsListView,
    GroupAdminsDetailView,
    InvitationsListView,
    InvitationDetailView,
)

app_name = "users"
urlpatterns = [
    # User profiles
    path("", UserListView.as_view()),
    path("me/", CurrentUserProfileView.as_view()),
    path("<int:pk>", UserProfileView.as_view()),
    # Friends
    path("friends/", FriendsListView.as_view()),
    path("friends/<int:pk>", FriendDetailView.as_view()),
    # Groups
    path("usergroups/", GroupsListView.as_view()),
    path("usergroups/<int:pk>", GroupsDetailView.as_view()),
    path("usergroups/<int:pk>/members/", GroupMembersListView.as_view()),
    path("usergroups/<int:pk>/members/<int:user_pk>", GroupMembersDetailView.as_view()),
    path("usergroups/<int:pk>/admins/", GroupAdminsListView.as_view()),
    path("usergroups/<int:pk>/admins/<int:user_pk>", GroupAdminsDetailView.as_view()),
    # Invitations
    path("invitations/", InvitationsListView.as_view()),
    path("invitations/<int:pk>", InvitationDetailView.as_view()),
]
