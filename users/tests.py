
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        # Create an existing user + token for authenticated tests
        self.existing_user = User.objects.create_user(
            username="existing",
            email="existing@example.com",
            password="password123"
        )
        self.existing_token = Token.objects.create(user=self.existing_user)

    def test_register_creates_user_and_token(self):
        """
        POST /api/users/register/ should create a user and a token.
        """
        url = reverse("users:user-create")  # resolves to /api/users/register/
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "pass1234"
        }

        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Check user exists in DB
        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "new@example.com")

        # Token should exist
        self.assertTrue(Token.objects.filter(user=user).exists())

        # Password should not be returned in response
        self.assertNotIn("password", resp.data)

    def test_login_returns_token(self):
        """
        POST /api/users/login/ returns the token for correct credentials.
        """
        url = reverse("users:login")  # resolves to /api/users/login/
        resp = self.client.post(url, {
            "username": "existing",
            "password": "password123"
        }, format="json")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("token", resp.data)
        self.assertEqual(resp.data["token"], self.existing_token.key)

    def test_user_list_requires_authentication_and_returns_list(self):
        """
        GET /api/users/ should require token and return user list when authenticated.
        """
        url = reverse("users:user-list")  # resolves to /api/users/

        # No auth -> unauthorized
        resp = self.client.get(url, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Authenticated request
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.existing_token.key)
        resp = self.client.get(url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.data, list)

        # Existing user should appear in response
        usernames = [u.get("username") for u in resp.data]
        self.assertIn("existing", usernames)

    def test_register_duplicate_email_fails(self):
        """
        Trying to register with an email that already exists should return 400.
        """
        User.objects.create_user(username="alpha", email="dup@example.com", password="pass1")

        url = reverse("users:user-create")
        payload = {"username": "beta", "email": "dup@example.com", "password": "pass2"}
        resp = self.client.post(url, payload, format="json")

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "email" in resp.data or "non_field_errors" in resp.data or "detail" in resp.data
        )
