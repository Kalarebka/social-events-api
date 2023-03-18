from abc import ABC, abstractmethod, abstractproperty

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import InvitationsPermission


class AbstractInvitationDetailView(ABC, APIView):
    """Handle different types of invitations.
    GET - get single invitation details
    DELETE - delete the invitation (only in response not received)
    """

    permission_classes = [InvitationsPermission]

    @abstractmethod
    def get_serializer(self, obj):
        """Return serializer with the invitation data"""
        pass

    @abstractmethod
    def get_invitation_model(self):
        """Return concrete invitation model"""
        pass

    def get(self, request, pk):
        """GET - Single invitation details"""
        invitation = get_object_or_404(self.get_invitation_model(), pk=pk)
        self.check_object_permissions(request, invitation)
        serializer = self.get_serializer(invitation)
        return Response(serializer.data)

    def delete(self, request, pk):
        """DELETE: cancel the invitation"""
        invitation = get_object_or_404(self.get_invitation_model(), pk=pk)
        self.check_object_permissions(request, invitation)

        if invitation.response_received:
            return Response(
                {"detail": "Response already received, invitation cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AbstractInvitationResponseView(ABC, APIView):
    # TODO break into 2 views, email response separate
    """
    Receive responses to invitations
    """

    @abstractmethod
    def get_invitation_model(self):
        """Return concrete invitation model"""
        pass

    def get(self, request, pk):
        """Respond by following a url in the invitation email"""
        invitation = get_object_or_404(self.get_invitation_model(), pk=pk)
        token = request.query_params.get("token", None)
        invitation_response = request.query_params.get("response", None)

        # Check if the right token is provided
        if token != invitation.email_response_token:
            return Response(
                {"detail": "invalid token"}, status=status.HTTP_403_FORBIDDEN
            )

        # Check if response query parameter value is valid
        if invitation_response in ["accept", "decline"]:
            invitation.send_response(invitation_response)
            return Response(status=status.HTTP_200_OK)

        return Response(
            {"error": "Response must be one of the following: accept or decline"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def post(self, request, pk):
        """
        Send response to an invitation
            Query parameter:
            - response: accept/decline
        """
        invitation_response = request.query_params.get("response", None)
        invitation = get_object_or_404(self.get_invitation_model(), pk=pk)
        if request.user != invitation.receiver:
            return Response(
                {"detail": "You're not allowed to respond to this invitation"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if invitation_response in ["accept", "decline"]:
            invitation.send_response(invitation_response)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"error": "Response must be one of the following: accept or decline"},
            status=status.HTTP_400_BAD_REQUEST,
        )
