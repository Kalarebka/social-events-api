from django.contrib.auth import get_user_model
from django.test import TestCase

from messagebox.models import Message

User = get_user_model()


class MessageTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = User.objects.create_user(
            email="ika@ika.com", username="ika", password="somepassword"
        )
        cls.user2 = User.objects.create_user(
            email="eryk@eryk.com", username="eryk", password="anotherpassword"
        )
        cls.message1 = Message.objects.create(
            sender=cls.user1,
            receiver=cls.user2,
            title="Message Title",
            content="some message content",
        )

    def test_message_model(self):
        self.assertEqual(self.message1.sender, self.user1)
        self.assertEqual(self.message1.receiver, self.user2)
        self.assertEqual(self.message1.title, "Message Title")
        self.assertEqual(self.message1.content, "some message content")
        self.assertEqual(self.message1.read_status, False)
        self.assertEqual(str(self.message1), "Message Title")
