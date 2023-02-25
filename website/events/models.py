from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from users.models import UserGroup, AbstractInvitation


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
    """Creates recurring events according to schedule and keeps track of all related events."""

    FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]
    interval = models.IntegerField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    # start_datetime - use the base event's start datetime
    end_datetime = models.DateTimeField(null=True, blank=True)
    repeats = models.IntegerField(null=True, blank=True)

    def clean(self):
        if not self.end_datetime and not self.repeats:
            raise ValidationError(
                "Either end date or number of repeats must be provided."
            )

    def schedule_events(self):
        # when created - create events according to the schedule with schedule foreign key set to self
        events_to_schedule = []
        Event.objects.bulk_create(events_to_schedule)

    def delete_all_events(self):
        # cancel all events scheduled by the scheduler
        pass


class Event(models.Model):

    # TextChoices enums
    class EventType(models.TextChoices):
        PRIVATE = ("private", "Private Event")
        GROUP = ("group", "Group Event")

    class EventStatus(models.TextChoices):
        PLANNED = ("planned", "Planned")
        IN_PROGRESS = ("in progress", "In progress")
        ENDED = ("ended", "Ended")
        CANCELLED = ("cancelled", "Cancelled")
11
    # Basic info
    event_type = models.CharField(choices=EventType.choices, max_length=15)
    name = models.CharField(max_length=128)
    description = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=EventStatus.choices, max_length=11, default=EventStatus.PLANNED
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, blank=True, null=True
    )

    # Group and users
    group = models.ForeignKey(
        UserGroup, default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    organisers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="events_as_organiser"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="events_as_participant",
        through="EventInvitation",
        through_fields=("event", "receiver"),
    )

    # Recurring events
    recurrence_schedule = models.ForeignKey(
        RecurringEventSchedule,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
        related_name="scheduled_events",
    )

    def save(self, *args, **kwargs):
        # if creating the event (!!!!or if start/end date was changed),
        # create a task to change event status at that time
        # if event type is group event, send invitations to all group members
        super().save(*args, **kwargs)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Event end date must be later than start date")

        if self.event_type == "group" and self.group is None:
            raise ValidationError("Group events must have group defined.")


class EventInvitation(AbstractInvitation):
    # from abstract invitation:
    # - sender, receiver, confirmed bool, response_received bool, date_sent
    # - methods: save, send_invitation_email, send_response
    # - to implement: confirm
    # - override the save() method to not send emails separately but in batches for inviting a list of users?

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=False,
        related_name="invited_users",
    )

    def confirm(self):
        self.confirmed = True

    @property
    def get_invitation_email_template(self):
        pass
