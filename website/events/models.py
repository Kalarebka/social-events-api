from dateutil.rrule import rrule

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from invitations.models import AbstractInvitation, AbstractEmailInvitation
from users.models import UserGroup
from .constants import EventType, EventStatus, FrequencyChoices, FREQUENCY_MAP


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


class Event(models.Model):

    # Basic info
    event_type = models.CharField(choices=EventType.choices, max_length=15)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=5000)
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
        settings.AUTH_USER_MODEL, related_name="organised_events"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="events",
        through="EventInvitation",
        through_fields=("event", "receiver"),
    )
    recurrence_schedule = models.ForeignKey(
        "RecurringEventSchedule",
        null=True,
        blank=True,
        related_name="events",
        on_delete=models.SET_NULL,
    )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Event end date must be later than start date")

        if self.event_type == "group" and self.group is None:
            raise ValidationError("Group events must have group defined.")


class RecurringEventSchedule(models.Model):
    """Create recurring events according to schedule and keep track of all related events."""

    interval = models.IntegerField()
    frequency = models.CharField(max_length=10, choices=FrequencyChoices.choices)
    end_datetime = models.DateTimeField(null=True, blank=True)
    repeats = models.IntegerField(null=True, blank=True)
    base_event = models.OneToOneField(
        Event, null=False, related_name="based_schedule", on_delete=models.CASCADE
    )

    def clean(self):
        if not self.end_datetime and not self.repeats:
            raise ValidationError(
                "Either end date or number of repeats must be provided."
            )

    def schedule_events(self):
        """Create events according to the schedule with schedule foreign key set to self"""
        # need to figure out how to do invitations/responses to recurring events first
        pass

    def calculate_dates_to_schedule(self):
        start_date = self.base_event.start_date
        frequency = FREQUENCY_MAP[self.frequency]
        if self.end_datetime:
            end_date = self.end_datetime
            dates = list(
                rrule(
                    dtstart=start_date,
                    until=end_date,
                    freq=frequency,
                    interval=self.interval,
                )
            )
        elif self.repeats:
            dates = list(
                rrule(
                    dtstart=start_date,
                    count=self.repeats,
                    freq=frequency,
                    interval=self.interval,
                )
            )
        else:
            raise ValueError("Either end date or number of repeats must be provided.")
        return dates

    def cancel_all_events(self):
        events = self.events.all()
        for event in events:
            event.status = EventStatus.CANCELLED


class EventInvitation(AbstractEmailInvitation, AbstractInvitation):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=False,
        related_name="invited_users",
    )

    def confirm(self):
        if self.event.recurrence_schedule:
            # TODO add user as confirmed to all events in the schedule
            pass

    def get_email_template(self) -> str:
        return "invitation_emails/event_invitation.html"

    def get_email_data(self):
        data = {}
        data["receiver_name"] = self.receiver.username
        data["event_name"] = self.event.name
        data["confirm_url"] = self.get_response_url("accept")
        data["decline_url"] = self.get_response_url("decline")
        return data

    def get_subject(self):
        return f"You have been invited to {self.event.name}"

    def get_recipient_list(self):
        return [
            self.receiver.email,
        ]

    def get_response_url(self):
        # TODO
        pass
