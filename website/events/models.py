from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    TextChoices,
    TextField,
)
from users.models import UserGroup


class Location(Model):
    name = CharField(max_length=64)
    latitude = FloatField()
    longitude = FloatField()
    country = CharField(max_length=32, blank=True, null=True)
    city = CharField(max_length=32, blank=True, null=True)
    street = CharField(max_length=32, blank=True, null=True)
    street_number = CharField(max_length=8, blank=True, null=True)
    zip_code = CharField(max_length=10, blank=True, null=True)
    saved_by = ManyToManyField(settings.AUTH_USER_MODEL, related_name="saved_locations")


class RecurringEventSchedule(Model):
    # prototype
    interval = IntegerField()
    time_unit = CharField(
        max_length=16
    )  # text choices for time units: day, weekday, etc.
    start_datetime = DateTimeField()
    end_datetime = DateTimeField()

    def schedule_events(self):
        # when created - create events according to the schedule with schedule foreign key set to self
        pass

    def delete_all_events(self):
        # delete all events scheduled by the scheduler
        pass


class Event(Model):
    class EventType(TextChoices):
        PERSONAL = "personal"
        GROUP = "group"

    class EventStatus(TextChoices):
        PLANNED = "planned"
        IN_PROGRESS = "in progress"
        ENDED = "ended"

    event_type = CharField(choices=EventType.choices, max_length=15)
    name = CharField(max_length=128)
    description = TextField()
    time_created = DateTimeField(auto_now_add=True)
    organisers = ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="events_as_organiser"
    )
    group = ForeignKey(UserGroup, on_delete=CASCADE, null=True, blank=True)
    participants = ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="events_as_participant"
    )  # throw this away and use invited_users/confirmed=True?
    start_time = DateTimeField()
    end_time = DateTimeField()
    location = ForeignKey(Location, on_delete=SET_NULL, blank=True, null=True)
    status = CharField(
        choices=EventStatus.choices, max_length=11, default=EventStatus.PLANNED
    )
    recurrence_schedule = ForeignKey(
        RecurringEventSchedule, on_delete=SET_NULL, default=None, null=True
    )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Event end date must be later than start date")


class EventInvitation(Model):
    event = ForeignKey(
        Event,
        on_delete=CASCADE,
        null=False,
        related_name="invited_users",
    )
    receiver = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="event_invitations",
    )
    confirmed = BooleanField(default=False)
