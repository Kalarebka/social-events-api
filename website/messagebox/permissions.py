from rest_framework.permissions import BasePermission


class MessageSenderOrReceiver(BasePermission):
    """Limits access to message to sender and receiver"""

    def has_object_permission(self, request, view, obj):
        if (obj.receiver == request.user) or (obj.sender == request.user):
            return True
        return False


class MessageThreadOwner(BasePermission):
    """Acces to message thread restricted to the thread users"""

    def has_object_permission(self, request, view, obj):
        if obj.user1 == request.user or obj.user2 == request.user:
            return True
        return False
