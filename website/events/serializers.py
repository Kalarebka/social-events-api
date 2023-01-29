from rest_framework import serializers

from .models import Event, Location


class EventRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "event_type",
            "description",
            "time_created",
            # "organisers",
            # "participants",
            "start_time",
            "end_time",
            "location",  # Full location info
            "status",
            "recurrence_schedule_id",
        ]


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "event_type",
            "description",
            "start_time",
            "end_time",
            "location_id",  # Id only
            "recurrence_schedule_id",
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["saved_by"]

    # add validators for address fields
