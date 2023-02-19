from rest_framework.permissions import BasePermission

from .models import UserGroup


class OwnProfileOrReadOnly(BasePermission):
    """User can update only their own profile."""

    def has_object_permission(self, request, view, obj):
        if obj.pk == request.user.pk or request.method == "GET":
            return True
        return False


# TODO merge the 2 permissions below?
class UserGroupPermission(BasePermission):
    """Only members can see group details, only admins can update and delete groups."""

    def has_object_permission(self, request, view, obj):
        if (
            request.user in obj.administrators
            or request.user in obj.members
            and request.method == "GET"
        ):
            return True
        return False


class IsGroupAdmin(BasePermission):
    """For actions that can only be performed by the group admin"""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, UserGroup):
            return request.user in obj.administrators
        return True


class InvitationsPermission(BasePermission):
    """Sender can retrieve the invitation and delete it
    Receiver can retrieve, delete and post response to the invitation"""

    def has_object_permission(self, request, view, obj):
        if (
            obj.sender == request.user
            and request.method in ["GET", "DELETE"]
            or obj.receiver == request.user
        ):
            return True
        return False
