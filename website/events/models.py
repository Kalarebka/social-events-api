from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    street = models.CharField(max_length=32, blank=True, null=True)
    street_number = models.CharField(max_length=8, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    saved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="saved_locations"
    )


class RecurringEventSchedule(models.Model):
    interval = models.IntegerField()
    time_unit = models.CharField(
        max_length=16
    )  # text choices for time units: day, weekday, etc.
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def schedule_events(self):
        # when created - create events according to the schedule with schedule foreign key set to self
        pass

    def delete_all_events(self):
        # delete all events scheduled by the scheduler
        pass


class Event(models.Model):
    class EventAccess(models.TextChoices):
        PERSONAL = "personal"
        GROUP = "group"

    class EventStatus(models.TextChoices):
        PLANNED = "planned"
        IN_PROGRESS = "in progress"
        ENDED = "ended"

    event_type = models.CharField(choices=EventAccess.choices, max_length=15)
    name = models.CharField(max_length=128)
    description = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    organisers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="events_as_organiser"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="events_as_participant"
    )  # throw this away and use invited_users/confirmed=True?
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, blank=True, null=True
    )
    status = models.CharField(
        choices=EventStatus.choices, max_length=11, default=EventStatus.PLANNED
    )
    recurrence_schedule = models.ForeignKey(
        RecurringEventSchedule, on_delete=models.SET_NULL, default=None, null=True
    )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Event end date must be later than start date")


class EventInvitation(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=False,
        related_name="invited_users",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_invitations",
    )
    confirmed = models.BooleanField(default=False)
