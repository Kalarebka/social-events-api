from rest_framework.permissions import BasePermission

from .models import UserGroup


class OwnProfileOrReadOnly(BasePermission):
    """User can update only their own profile."""

    def has_object_permission(self, request, view, obj):
        if obj.pk == request.user.pk or request.method == "GET":
            return True
        return False


class UserGroupPermission(BasePermission):
    """Limit permissions for usergroups to group members (GET only) and admins."""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, UserGroup):
            return (
                request.user in obj.administrators.all()
                or request.user in obj.members.all()
                and request.method == "GET"
            )
        return True


class InvitationsPermission(BasePermission):
    """Sender and receiver can retrieve and delete invitation"""

    def has_object_permission(self, request, view, obj):
        if (
            obj.sender == request.user
            and request.method in ["GET", "DELETE"]
            or obj.receiver == request.user
        ):
            return True
        return False
