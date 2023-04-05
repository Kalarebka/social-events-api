from abc import ABC, abstractmethod
from builtins import NotImplementedError

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import InvitationsPermission


class AbstractInvitationViewBase(ABC):
    """
    Abstract base that provides invitation model attribute and method for other views.

    Set invitation_model attribute or override get_invitation_model (defaults to self.invitation_model)

    """

    invitation_model = None

    def get_invitation_model(self):
        """Return concrete invitation model. Defaults to self.invitation_model."""
        if self.invitation_model:
            return self.invitation_model
        raise NotImplementedError(
            "The view should either include an invitation_model attribute, "
            "or override the get_invitation_model() method."
        )


class AbstractInvitationListView(AbstractInvitationViewBase, ListAPIView):
    """
    Abstract base for a list view for invitations.

    Additionally, you need to set the 'serializer_class' attribute or override 'get_serializer_class' method

    Uses basic invitation permissions - invitation sender and recipient have object permission.
    Returns received messages by default, category can be chosen with a query parameter:
    - category: "received" (default) or "sent"
    """

    permission_classes = [InvitationsPermission]

    def get_queryset(self):
        # Returns a list of invitations in which request.user is sender or recipient
        qs = self.get_invitation_model().objects.all()
        user = self.request.user

        category = self.request.query_params.get("category")
        if category == "sent":
            return qs.filter(sender=user)
        return qs.filter(recipient=user, response_received=False)


class AbstractInvitationDetailView(AbstractInvitationViewBase, RetrieveDestroyAPIView):
    """Handle different types of invitations.
    GET - get single invitation details
    DELETE - delete the invitation (only in response not received)

    Additionally, you need to set the 'serializer_class' attribute or override 'get_serializer_class' method
    """

    permission_classes = [InvitationsPermission]

    def get_queryset(self):
        return self.get_invitation_model().objects.all()

    def destroy(self, request, *args, **kwargs):
        """DELETE: cancel the invitation"""
        invitation = self.get_object()
        self.check_object_permissions(request, invitation)

        if invitation.response_received:
            return Response(
                {"detail": "Response already received, invitation cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AbstractInvitationResponseView(AbstractInvitationViewBase, APIView):
    """
    Receive response to an invitation through a POST request

    Query parameter: response ("accept"/"decline")
    """

    def post(self, request, pk):
        invitation = get_object_or_404(self.get_invitation_model(), pk=pk)
        if request.user != invitation.recipient:
            return Response(
                {"detail": "You're not allowed to respond to this invitation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        invitation_response = request.query_params.get("response", None)
        if invitation_response not in ["accept", "decline"]:
            return Response(
                {"error": "Response must be one of the following: accept or decline"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.send_response(invitation_response)
        return Response(status=status.HTTP_200_OK)


class AbstractEmailInvitationResponseView(AbstractInvitationViewBase, APIView):
    """
    Receive response to an invitation through a GET request (for use in emails)

    Query parameters:
    - response ("accept"/"decline")
    - token - authorization token to compare with invitation's email_response_token attribute
    """

    def get(self, request, pk):
        invitation = get_object_or_404(self.get_invitation_model(), pk=pk)
        token = request.query_params.get("token", None)

        # Check if the right token is provided
        if token != invitation.email_response_token:
            return Response(
                {"detail": "invalid token"}, status=status.HTTP_403_FORBIDDEN
            )

        invitation_response = request.query_params.get("response", None)

        # Check if response query parameter value is valid
        if invitation_response not in ["accept", "decline"]:
            return Response(
                {"error": "Response must be one of the following: accept or decline"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.send_response(invitation_response)
        return Response(status=status.HTTP_200_OK)
