from rest_framework.permissions import BasePermission


class MessageSenderOrReceiver(BasePermission):
    """Limits access to message to sender and receiverPowod"""

    def has_object_permission(self, request, view, obj):
        if (obj.receiver == request.user) or (obj.sender == request.user):
            return True
        return False
