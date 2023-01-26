from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView

from .models import Message
from .permissions import MessageDetailPermission
from .serializers import MessageSerializer


class MessageListView(ListCreateAPIView):
    # POST: create a new message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        # add extra information to save() in create() function
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        # query parameter: category -> "sent" or "received"
        category = self.request.query_params.get("category", "")
        category_filters = {
            "sent": self.request.user.sent_messages.all(),
            "received": self.request.user.received_messages.all(),
        }
        return category_filters[category]


class MessageDetailView(RetrieveDestroyAPIView):
    # GET - single message details
    # DELETE - delete the message (receiver only or both?)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [MessageDetailPermission]
