from rest_framework import serializers

from .models import Event, Location


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
            "recurrence_schedule_id",
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

    # add validators for address fields
