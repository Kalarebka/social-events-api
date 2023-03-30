from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event
from .tasks import update_event_status


@receiver(post_save, sender=Event)
def set_update_event_status_task(
    sender, instance, created, update_fields=None, **kwargs
):
    if created:
        # Schedule status update to run at start and end times
        update_event_status.apply_async(args=[instance.id], eta=instance.start_time)
        update_event_status.apply_async(args=[instance.id], eta=instance.end_time)
    elif update_fields:
        if "start_time" in update_fields:
            # Schedule status update to run at start time
            update_event_status.apply_async(args=[instance.id], eta=instance.start_time)
        if "end_time" in update_fields:
            # Schedule status update to run at end time
            update_event_status.apply_async(args=[instance.id], eta=instance.end_time)
