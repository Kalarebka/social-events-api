from django.db.models import Q

from .models import MessageThread


def get_message_thread(user_1, user_2):
    try:
        message_thread = MessageThread.objects.get(
            Q(user1=user_1, user2=user_2) | Q(user1=user_2, user2=user_1)
        )
        return message_thread
    except MessageThread.DoesNotExist:
        return None
