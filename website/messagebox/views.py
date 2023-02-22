from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response


from .models import Message
from .permissions import MessageSenderOrReceiver
from .serializers import MessageSerializer


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
                deleted_by_receiver=False
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
    permission_classes = [MessageSenderOrReceiver]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.read_status is False and request.user == instance.receiver:
            instance.read_status = True
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.sender == self.request.user:
            instance.deleted_by_sender = True
        else:
            instance.delete_by_receiver = True
        instance.save()
