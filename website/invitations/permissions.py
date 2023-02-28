from rest_framework.permissions import BasePermission


class InvitationsPermission(BasePermission):
    """Sender and receiver can retrieve and delete invitation"""

    def has_object_permission(self, request, view, obj):
        if obj.sender == request.user or obj.receiver == request.user:
            return True
        return False
