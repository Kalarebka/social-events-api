from rest_framework.permissions import BasePermission


class EventPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # if obj instance of event:
        #    if user in obj.participants: return True
        #    if obj.group return user in group.members
        return True
