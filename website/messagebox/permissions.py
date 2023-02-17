from rest_framework.permissions import BasePermission


class MessageDetailPermission(BasePermission):
    # only sender and receiver have access to the message
    def has_object_permission(self, request, view, obj):
        if (obj.receiver == request.user) or (obj.sender == request.user):
            return True
        return False
