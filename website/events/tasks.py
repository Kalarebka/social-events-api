from celery import shared_task
from django.utils import timezone

from .constants import EventStatus
from .models import Event


@shared_task
def update_event_status(event: Event):
    """Check if event status matches start and end times and update if necessary"""
    if event.status == EventStatus.CANCELLED:
        pass
    current_time = timezone.now()
    event_status_options = {
        (True, False): EventStatus.PLANNED,
        (False, False): EventStatus.IN_PROGRESS,
        (False, True): EventStatus.ENDED,
    }
    calculated_status = event_status_options(
        (current_time < event.start_time, current_time > event.end_time)
    )
    if calculated_status != event.status:
        event.status = calculated_status
        event.save(update_fields=["status"])
