from django.db import models


class EventType(models.TextChoices):
    PRIVATE = ("private", "Private Event")
    GROUP = ("group", "Group Event")


class EventStatus(models.TextChoices):
    PLANNED = ("planned", "Planned")
    IN_PROGRESS = ("in progress", "In progress")
    ENDED = ("ended", "Ended")
    CANCELLED = ("cancelled", "Cancelled")


class FrequencyChoices(models.TextChoices):
    DAILY = ("daily", "Daily")
    WEEKLY = ("weekly", "Weekly")
    MONTHLY = ("monthly", "Monthly")
