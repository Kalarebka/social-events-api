from .base_views import (
    AbstractEmailInvitationResponseView,
    AbstractInvitationDetailView,
    AbstractInvitationListView,
    AbstractInvitationResponseView,
)
from .models import BasicEmailInvitation, BasicInvitation
from .serializers import BasicEmailInvitationSerializer, BasicInvitationSerializer


class InvitationListView(AbstractInvitationListView):
    """
    List BasicInvitations for current user

    Uses basic invitation permissions - invitation sender and recipient have object permission.
    Query parameters:
    - category: "received" (default) or "sent"
    """

    def get_serializer_class(self):
        return BasicInvitationSerializer

    def get_invitation_model(self):
        return BasicInvitation


class EmailInvitationListView(AbstractInvitationListView):
    """
    List BasicEmailInvitations for current user

    Uses basic invitation permissions - invitation sender and recipient have object permission.
    Query parameters:
    - category: "received" (default) or "sent"
    """

    def get_serializer_class(self):
        return BasicEmailInvitationSerializer

    def get_invitation_model(self):
        return BasicEmailInvitation


class InvitationDetailView(AbstractInvitationDetailView):
    def get_serializer_class(self):
        return BasicInvitationSerializer

    def get_invitation_model(self):
        return BasicInvitation


class EmailInvitationDetailView(AbstractInvitationDetailView):
    def get_serializer_class(self):
        return BasicEmailInvitationSerializer

    def get_invitation_model(self):
        return BasicEmailInvitation


class InvitationResponseView(AbstractInvitationResponseView):
    def get_invitation_model(self):
        return BasicInvitation


class EmailInvitationResponseView(AbstractInvitationResponseView):
    def get_invitation_model(self):
        return BasicInvitation


class EmailInvitationEmailResponseView(AbstractEmailInvitationResponseView):
    def get_invitation_model(self):
        return BasicInvitation
