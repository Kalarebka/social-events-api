from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from messagebox.models import Message

User = get_user_model()


class MessageTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password1"
        )
        user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password2"
        )
        cls.message1 = Message.objects.create(
            sender=user1,
            recipient=user2,
            title="Message Title",
            content="some message content 1",
        )
        cls.message2 = Message.objects.create(
            sender=user1,
            recipient=user2,
            title="Message Title",
            content="some message content 2",
        )
        cls.message3 = Message.objects.create(
            sender=user2,
            recipient=user1,
            title="Message Title",
            content="some message content 3",
        )

    def setUp(self):
        self.user = User.objects.get(username="user1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_sent_messages_list_view(self):
        url = reverse("messagebox:message_list")
        response = self.client.get(url, {"category": "sent"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["sender"], self.user.pk)

    def test_received_messages_list_view(self):
        url = reverse("messagebox:message_list")
        response = self.client.get(url, {"category": "received"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["recipient"], self.user.pk)

    def test_messages_list_view_without_category_parameter(self):
        # Should default to received messages
        url = reverse("messagebox:message_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["recipient"], self.user.pk)
