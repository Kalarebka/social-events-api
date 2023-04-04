from rest_framework.permissions import BasePermission


class InvitationsPermission(BasePermission):
    """Sender and recipient can retrieve and delete invitation"""

    def has_object_permission(self, request, view, obj):
        if obj.sender == request.user or obj.recipient == request.user:
            return True
        return False
