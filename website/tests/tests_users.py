from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from users.models import CustomUser


class UsersTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create_user(
            username="user1", email="user1@example.com", password="password1"
        )
        CustomUser.objects.create_user(
            username="user2", email="user2@example.com", password="password2"
        )
        CustomUser.objects.create_user(
            username="user3", email="user3@example.com", password="password3"
        )
        CustomUser.objects.create_user(
            username="user4", email="user4@example.com", password="password4"
        )
        CustomUser.objects.create_user(
            username="user5", email="user5@example.com", password="password5"
        )
        CustomUser.objects.create_user(
            username="user6", email="user6@example.com", password="password6"
        )

    def setUp(self):
        self.user = CustomUser.objects.get(username="user1")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_list(self):
        url = reverse("users:user_list")
        response = self.client.get(url)
        self.assertEqual(self.user.is_authenticated, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 6)
