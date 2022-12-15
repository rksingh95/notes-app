from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from DjangoNotesApp.app.models import Note


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        user = get_user_model()
        self.user = user.objects.create_user(username="testuser", password="testpass")
        self.notes = Note.objects.create(
            title="12345678", tag="124", body="abcderfgrt", user_id=self.user.id
        )
