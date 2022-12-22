from rest_framework import serializers

from .models import Event, Location


class EventSerializer(serializers.ModelSerializer):

    # serialize nested models e.g. user = UserSerializer()
    #

    class Meta:
        model = Event
        fields = [
            "name",
            "event_access",
            "description",
            "time_created",
            "organisers",
            "start_time",
            "end_time",
            "location",
            "status",
        ]

        # https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        def create(self, validated_data):
            # create the Event object with nested models (organisers, location)
            pass

        def update(self, instance, validated_data):
            # update the instance
            pass


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
