from django.urls import path

from .views import ReceivedMessagesView


app_name = "messagebox"
urlpatterns = {
    path("", ReceivedMessagesView.as_view())
}