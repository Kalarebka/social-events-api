from rest_framework.permissions import BasePermission


class OwnProfileOrReadOnly(BasePermission):
    """User can update only their own profile."""

    def has_object_permission(self, request, view, obj):
        if obj.pk == request.user.pk or request.method == "GET":
            return True
        return False
