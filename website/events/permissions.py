from rest_framework.permissions import BasePermission

from .models import Event


class EventPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Event):
            if obj.group:
                return request.user in obj.group.members
            return obj in request.user.events

        return True
