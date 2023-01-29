from rest_framework.permissions import BasePermission


class EventPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # If event is public, all authenticated users can see it, and only organiser can update or delete
        # If event is invitation only, organisers and participants can see it
        return True
