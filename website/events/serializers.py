from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Event, Location, RecurringEventSchedule, EventInvitation


class EventRetrieveSerializer(serializers.ModelSerializer):
    organiser_ids = serializers.SerializerMethodField("get_organiser_ids")
    participant_ids = serializers.SerializerMethodField("get_participant_ids")

    class Meta:
        model = Event
        fields = [
            "name",
            "event_type",
            "description",
            "time_created",
            "organiser_ids",
            "participant_ids",
            "start_time",
            "end_time",
            "location_id",
            "status",
        ]

    def get_organiser_ids(self, obj):
        return [organiser.id for organiser in obj.organisers.all()]

    def get_participant_ids(self, obj):
        return [user.id for user in obj.participants.all()]


class EventRetrieveMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["name", "event_type"]


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "name",
            "event_type",
            "description",
            "start_time",
            "end_time",
            "location_id",
            "recurrence_schedule_id",
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ["saved_by"]

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise ValidationError("Longitude must be between -180 and 180.")
        return value


class RecurringEventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringEventSchedule
        fields = ["id", "interval", "frequency", "end_datetime", "repeats"]


class EventInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInvitation
