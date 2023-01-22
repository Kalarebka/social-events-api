from rest_framework.permissions import BasePermission

# All messages
class MessageDetailPermission(BasePermission):
    # custom permission
    # One message:
    # sender can GET the message
    # receiver can GET and DELETE the message
    def has_object_permission(self, request, view, obj):
        if (obj.receiver == request.user) or (
            obj.sender == request.user and request.method == "GET"
        ):
            return True
        return False
