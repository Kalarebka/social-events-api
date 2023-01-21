from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer


class MessageListView(ListCreateAPIView):
    # GET: return list of received messages sorted by date (newest first)
    # query_params.category: sent/received
    # POST: create a new message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    # def get_queryset(self):
    #     # return current user's received/sent messages
    #     if self.request.query_params


class MessageDetailView(RetrieveDestroyAPIView):
    # GET - single message details
    # DELETE - delete the message (receiver only)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
