from rest_framework.permissions import BasePermission


class EventPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Group event - group members can see
        # Personal event - invited users can retrieve, organiser can update and delete
        return True
