from rest_framework import serializers

from .models import Event, Location


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "event_access",
            "description",
            "time_created",
            "organisers",
            "participants",
            "start_time",
            "end_time",
            "location",
            "status",
        ]
        read_only_fields = ["time_created"]

        def create(self, validated_data, user):
            pass


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
