from django.urls import path

from .views import (
    FriendDetailView,
    FriendInvitationDetailView,
    GroupAdminsDetailView,
    GroupInvitationDetailView,
    GroupMembersDetailView,
    GroupsDetailView,
    GroupsListView,
    InvitationsListView,
    UserListView,
    UserProfileView,
    FriendInvitationResponseView,
    FriendInvitationEmailResponseView,
    GroupInvitationResponseView,
    GroupInvitationEmailResponseView,
)

app_name = "users"
urlpatterns = [
    # User profiles
    path("", UserListView.as_view(), name="user_list"),
    path("<int:pk>", UserProfileView.as_view(), name="user_profile"),
    # Friends
    path("friends/<int:friend_pk>", FriendDetailView.as_view(), name="friend_detail"),
    # Groups
    path("usergroups/", GroupsListView.as_view(), name="groups_list"),
    path("usergroups/<int:pk>", GroupsDetailView.as_view(), name="group_detail"),
    path(
        "usergroups/<int:group_pk>/members/<int:user_pk>",
        GroupMembersDetailView.as_view(),
    ),
    path(
        "usergroups/<int:group_pk>/admins/<int:user_pk>",
        GroupAdminsDetailView.as_view(),
    ),
    # Invitations
    path("invitations/", InvitationsListView.as_view(), name="invite_list"),
    path(
        "invitations/friends/<int:pk>",
        FriendInvitationDetailView.as_view(),
        name="friend_invite_detail",
    ),
    path(
        "invitations/groups/<int:pk>",
        GroupInvitationDetailView.as_view(),
        name="group_invite_detail",
    ),
    path(
        "invitations/friends/<int:pk>/response",
        FriendInvitationResponseView.as_view(),
        name="friend_invite_response",
    ),
    path(
        "invitations/friends/<int:pk>/email-response",
        FriendInvitationEmailResponseView.as_view(),
        name="friend_invite_email_response",
    ),
    path(
        "invitations/groups/<int:pk>/response",
        GroupInvitationResponseView.as_view(),
        name="group_invite_response",
    ),
    path(
        "invitations/groups/<int:pk>/email-response",
        GroupInvitationEmailResponseView.as_view(),
        name="group_invite_email_response",
    ),
]
