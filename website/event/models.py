from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Location(models.Model):
    # what about online events?
    name = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    street = models.CharField(max_length=32, blank=True, null=True)
    street_number = models.CharField(max_length=8, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    users_favorites = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Event(models.Model):
    class EventAccess(models.TextChoices):
        PRIVATE = "private"
        GROUP = "group"
        PUBLIC = "public"

    event_access = models.CharField(choices=EventAccess.choices, max_length=8)
    name = models.CharField(max_length=128)
    description = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    organisers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events_organiser") # needs some way to manage no organisers
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events_participant")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, blank=True, null=True
    )

    @property
    def status(self):
        if datetime.now() < self.start_time:
            return "planned"
        elif datetime.now() > self.end_time:
            return "ended"
        return "in progress"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Event end date must be later than start date")


# recurring events?
# event access differences?
