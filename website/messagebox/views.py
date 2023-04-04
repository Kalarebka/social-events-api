from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response

from .db_helpers import get_message_thread
from .models import Message, MessageThread
from .permissions import MessageSenderOrrecipient, MessageThreadOwner
from .serializers import MessageSerializer, MessageThreadSerializer


class MessageListView(ListCreateAPIView):
    """
    GET: retrieve a list of user's messages.
         Query parameter:
         - category: sent/received (default: received)
    POST: create and send a new message
    """

    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        # Set sender to current user when creating a message
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        category = self.request.query_params.get("category", "received")
        category_filters = {
            "sent": self.request.user.sent_messages.filter(deleted_by_sender=False),
            "received": self.request.user.received_messages.filter(
                deleted_by_recipient=False
            ),
        }
        return category_filters[category]


class MessageDetailView(RetrieveDestroyAPIView):
    """
    GET - Single message details.
    DELETE - Mark the message as deleted only for the user who deletes it.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [MessageSenderOrrecipient]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.read_status is False and request.user == instance.recipient:
            instance.read_status = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.sender == self.request.user:
            instance.deleted_by_sender = True
        else:
            instance.deleted_by_recipient = True
        instance.save()


class MessageThreadDetailView(RetrieveDestroyAPIView):
    """
    GET - retrieve message thread between the current user and user_id
    DELETE - delete all messages in the thread
    """

    queryset = MessageThread.objects.all()
    serializer_class = MessageThreadSerializer
    permission_classes = [MessageThreadOwner]

    def get_object(self):
        other_user_id = self.kwargs.get("user_pk")
        other_user = get_object_or_404(get_user_model(), pk=other_user_id)
        message_thread = get_message_thread(self.request.user, other_user)
        if not message_thread:
            raise Http404()
        return message_thread
