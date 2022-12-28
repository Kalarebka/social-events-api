from rest_framework.views import APIView

class ReceivedMessagesView(APIView):
    def get(self, request):
        # return list of received messages sorted by date (newest first), should be paginated
        pass

    def post(self, request):
        pass