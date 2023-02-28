from abc import ABC, abstractmethod

from django.shortcuts import get_object_or_404
from rest_framework import status


from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import (
    InvitationsPermission,
)


class AbstractInvitationDetailView(ABC, APIView):
    """Handle different types of invitations.
    GET - get single invitation details
    DELETE - delete the invitation (only in response not received)
    """

    permission_classes = [InvitationsPermission]

    @abstractmethod
    def get_serializer(self, qs):
        pass

    @abstractmethod
    def get_object(self, pk):
        pass

    def get(self, request, pk):
        """GET - Single invitation details"""
        invitation = self.get_object(pk)
        self.check_object_permissions(request, invitation)
        serializer = self.get_serializer(invitation)
        return Response(serializer.data)

    def delete(self, request, pk):
        """DELETE: cancel the invitation"""
        invitation = self.get_object(pk)
        self.check_object_permissions(request, invitation)

        if invitation.response_received:
            return Response(
                {"detail": "Response already received, invitation cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# TODO
# only receiver can respond to an invitation
# for confirmation by email - generate a token for each invitation, then send it in the email link
# -> in the get() method get object by token not by pk // or get by pk, but check token against the db
# in post() method get pk from url, check if user is invitation.receiver


class AbstractInvitationResponseView(ABC, APIView):
    """
    Receive responses to invitations
    """

    @abstractmethod
    def get_object(self):
        pass

    def get(self, request, pk):
        # Accepting by GET method for compatibility with invitation response links in email
        invitation_response = request.query_params.get("response", None)
        if invitation_response in ["accept", "decline"]:
            invitation = get_object_or_404(GroupInvitation, pk=pk)
            invitation.send_response(invitation_response)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"error": "Response must be one of the following: accept or decline"},
            status=status.HTTP_400_BAD_REQUEST,
        )
