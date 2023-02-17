from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView

from .models import Message
from .permissions import MessageDetailPermission
from .serializers import MessageSerializer


class MessageListView(ListCreateAPIView):
    """GET: retrieve a list of user's messages. Query parameter: category: sent/received
    POST: create a new message"""

    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        # add extra information to save() in create() function
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        # query parameter: category -> "sent" or "received"
        category = self.request.query_params.get("category", "received")
        category_filters = {
            "sent": self.request.user.sent_messages.filter(deleted_by_sender=False),
            "received": self.request.user.received_messages.filter(
                deleted_by_receiver=False
            ),
        }
        return category_filters[category]


class MessageDetailView(RetrieveDestroyAPIView):
    """GET - single message details
    DELETE - delete the message (sets deleted_by_sender or deleted_by_receiver to False,
             so the message won't show up on message list)"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [MessageDetailPermission]

    def perform_destroy(self, instance):
        if instance.sender == request.user:
            instance.deleted_by_sender = True
        else:
            instance.delete_by_receiver = True
        instance.save()
