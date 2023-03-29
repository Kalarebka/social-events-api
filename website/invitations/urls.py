from django.urls import path

from .views import (
    InvitationListView,
    InvitationDetailView,
    EmailInvitationDetailView,
    InvitationResponseView,
    EmailInvitationResponseView,
    EmailInvitationEmailResponseView,
)

app_name = "invitations"
urlpatterns = [
    path("", InvitationListView.as_view(), name="invitation_list"),
    path("<int:pk>/", InvitationDetailView.as_view(), name="invitation_detail"),
    path(
        "email-invitations/<int:pk>/",
        EmailInvitationDetailView.as_view,
        name="email_invitation_detail",
    ),
    path(
        "<int:pk>/response/",
        InvitationResponseView.as_view(),
        name="invitation_response",
    ),
    path("email-invitations/<int:pk>/response"),
]
