import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from DjangoNotesApp.app.models import Note
from DjangoNotesApp.app.tests.base_test_setup import BaseTest


class TestNotes(BaseTest):
    def setUp(self) -> None:
        super().setUp()

    @pytest.mark.django_db
    def test_add_notes(self):
        self.assertTrue(self.client.login(username="testuser", password="testpass"))
        response = self.client.post(
            "/addnote",
            {"notestitle": "123456789", "notesbody": "abcderfgrt", "notestag": "124"},
            follow=True,
        )
        note = Note.objects.get(title="123456789")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(note.title, "123456789")

    @pytest.mark.django_db
    def test_add_notes_with_samll_title_less_than_8_char(self):
        self.assertTrue(self.client.login(username="testuser", password="testpass"))
        response = self.client.post(
            "/addnote",
            {"notestitle": "123789", "notesbody": "abcderfgrt", "notestag": "124"},
            follow=True,
        )
        with self.assertRaises(Note.DoesNotExist):
            note = Note.objects.get(title="123456789")
            self.assertEqual(response.status_code, 200)

    @pytest.mark.django_db
    def test_edit_notes(self):
        self.assertTrue(self.client.login(username="testuser", password="testpass"))
        edit_note_url = "/edit/note/" + str(self.notes.id)
        response = self.client.post(edit_note_url, follow=True)
        self.assertEqual(response.status_code, 200)

    @pytest.mark.django_db
    def test_edit_notes_by_other_user(self):
        user = User.objects.create_user(username="testuser1", password="testpass1")
        notes = Note.objects.create(
            title="123456789", tag="1245", body="abcdfscderfgrt", user_id=user.id
        )
        self.assertTrue(self.client.login(username="testuser1", password="testpass1"))
        edit_note_url = "/edit/note/" + str(self.notes.id)
        response = self.client.post(edit_note_url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0].message, "Editing other user's notes is forbidden")

    @pytest.mark.django_db
    def test_update_notes(self):
        self.assertTrue(self.client.login(username="testuser", password="testpass"))
        edit_note_url = "/update/note/" + str(self.notes.id)
        response = self.client.post(
            edit_note_url,
            {
                "notestitle": "thermondonotes",
                "notesbody": "abcderfgrt",
                "notestag": "124",
            },
            follow=True,
        )
        note = Note.objects.get(title="thermondonotes")
        self.assertEqual(note.title, "thermondonotes")
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message, "Your note has been updated successfully")

    @pytest.mark.django_db
    def test_update_notes_with_invalid_title(self):
        self.assertTrue(self.client.login(username="testuser", password="testpass"))
        edit_note_url = "/update/note/" + str(self.notes.id)
        response = self.client.post(
            edit_note_url,
            {"notestitle": "ther", "notesbody": "abcderfgrt", "notestag": "124"},
            follow=True,
        )
        note = Note.objects.get(title="12345678")
        self.assertEqual(note.title, "12345678")
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(messages[0].message, "Please fill the form correctly")

    @pytest.mark.django_db
    def test_search_note_without_authentication_of_user(self):
        search_note_url = "/search/note/" + str(self.notes.tag)
        response = self.client.get(search_note_url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0].message, "User not authenticated")

    @pytest.mark.django_db
    def test_search_note_with_authentication_of_user(self):
        self.assertTrue(self.client.login(username="testuser", password="testpass"))
        search_note_url = "/search/note/" + str(self.notes.tag)
        response = self.client.get(search_note_url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        notes = Note.objects.get(title=self.notes.title)
        self.assertEqual(notes.tag, self.notes.tag)
        self.assertEqual(
            messages[0].message, "Please find the latest note with the tag"
        )

    @pytest.mark.django_db
    def test_delete_notes(self):
        self.assertTrue(self.client.login(username="testuser", password="testpass"))
        delete_note_url = "/delete/note/" + str(self.notes.id)
        response = self.client.delete(delete_note_url, follow=True)
        with self.assertRaises(Note.DoesNotExist):
            note = Note.objects.get(title="12345678")
            self.assertEqual(response.status_code, 200)
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(
                messages[0].message, "Your note has been deleted successfully"
            )

    @pytest.mark.django_db
    def test_delete_notes_of_other_user(self):
        User.objects.create_user(username="testuser1", password="testpass1")
        self.assertTrue(self.client.login(username="testuser1", password="testpass1"))
        delete_note_url = "/delete/note/" + str(self.notes.id)
        response = self.client.delete(delete_note_url, follow=True)

        note = Note.objects.get(title="12345678")
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            messages[0].message, "Deleting other user's notes is forbidden"
        )
