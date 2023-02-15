from django.urls import path

from .views import (
    FriendDetailView,
    FriendsListView,
    GroupAdminsDetailView,
    GroupAdminsListView,
    GroupMembersDetailView,
    GroupMembersListView,
    GroupsDetailView,
    GroupsListView,
    FriendInvitationDetailView,
    FriendInvitationsListView,
    UserListView,
    UserProfileView,
)

app_name = "users"
urlpatterns = [
    # User profiles
    path("", UserListView.as_view(), name="user_list"),
    path("<int:pk>", UserProfileView.as_view(), name="user_profile"),
    # Friends
    path("friends/", FriendsListView.as_view(), name="friends_list"),
    path("friends/<int:friend_pk>", FriendDetailView.as_view(), name="friend_detail"),
    # Groups
    path("usergroups/", GroupsListView.as_view(), name="groups_list"),
    path("usergroups/<int:pk>", GroupsDetailView.as_view(), name="group_detail"),
    path("usergroups/<int:pk>/members/", GroupMembersListView.as_view()),
    path("usergroups/<int:pk>/members/<int:user_pk>", GroupMembersDetailView.as_view()),
    path("usergroups/<int:pk>/admins/", GroupAdminsListView.as_view()),
    path("usergroups/<int:pk>/admins/<int:user_pk>", GroupAdminsDetailView.as_view()),
    # Invitations
    path("invitations/friends", FriendInvitationsListView.as_view()),
    path("invitations/friends/<int:pk>", FriendInvitationDetailView.as_view()),
]
