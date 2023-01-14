from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="Eryk", email="eryk@gmail.com", password="password12345"
        )
        self.assertEqual(user.username, "Eryk")
        self.assertEqual(user.email, "eryk@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="admin1", email="admin1@mail.com", password="admin12345"
        )
        self.assertEqual(user.username, "admin1")
        self.assertEqual(user.email, "admin1@mail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_no_email(self):
        User = get_user_model()
        user = User.objects.create_user(username="Eryk", password="password12345")
        self.assertEqual(user.username, "Eryk")
