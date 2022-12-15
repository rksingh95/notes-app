import pytest
from django.contrib.auth.models import User

from DjangoNotesApp.app.tests.base_test_setup import BaseTest


class TestUser(BaseTest):
    def setUp(self) -> None:
        super().setUp()

    @pytest.mark.django_db
    def test_login_user(self):
        response = self.client.post(
            "/profile/login",
            {"username": "testuser", "password": "testpass"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    @pytest.mark.django_db
    def test_login_invalid_credential_for_a_user(self):
        response = self.client.post(
            "/profile/login", {"username": "test", "password": "testpass"}, follow=True
        )
        self.assertEqual(response.status_code, 200)

    @pytest.mark.django_db
    def test_login_logout_user(self):
        response = self.client.post(
            "/profile/login",
            {"username": "testuser", "password": "testpass"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/logout", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_signup(self):
        response = self.client.post(
            "/profile/signup",
            {
                "username": "test",
                "email": "bac@gmail.com",
                "password": "testpass",
                "_password": "testpass",
            },
            follow=True,
        )
        user = User.objects.get(username="test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.username, "test")

    def test_username_validation_post_signup(self):
        response = self.client.post(
            "/profile/signup",
            {
                "username": 123,
                "email": "bac@gmail.com",
                "password": "testpass",
                "_password": "testpass",
            },
            follow=True,
        )
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username=123)
            self.assertEqual(response.status_code, 200)

    def test_user_password_validation_post_signup(self):
        response = self.client.post(
            "/profile/signup",
            {
                "username": "test",
                "email": "bac@gmail.com",
                "password": 123,
                "_password": "testpass",
            },
            follow=True,
        )
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username="test")
            self.assertEqual(response.status_code, 200)

    def test_user_password_length_less_than_6_validation_post_signup(self):
        response = self.client.post(
            "/profile/signup",
            {
                "username": "test",
                "email": "bac@gmail.com",
                "password": "test12",
                "_password": "testpass",
            },
            follow=True,
        )
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username="test")
            self.assertEqual(response.status_code, 200)

    def test_user_password_not_equal_to_repeat_password(self):
        response = self.client.post(
            "/profile/signup",
            {
                "username": "test",
                "email": "bac@gmail.com",
                "password": "testpas12",
                "_password": "testpass",
            },
            follow=True,
        )
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username="test")
            self.assertEqual(response.status_code, 200)

    def test_user_name_can_be_alpha_numeric(self):
        response = self.client.post(
            "/profile/signup",
            {
                "username": "test123",
                "email": "bac@gmail.com",
                "password": "testpass",
                "_password": "testpass",
            },
            follow=True,
        )
        user = User.objects.get(username="test123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.username, "test123")
