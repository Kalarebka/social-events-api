from django.urls import path

from .views import MessageDetailView, MessageListView

app_name = "messagebox"
urlpatterns = [
    path("", MessageListView.as_view()),
    path("<int:pk>", MessageDetailView.as_view()),
]
