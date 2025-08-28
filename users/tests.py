# users/tests.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserAPITests(APITestCase):
    def setUp(self):
        # Existing user + token for authenticated tests
        self.existing_user = User.objects.create_user(
            username="existing",
            email="existing@example.com",
            password="password123"
        )
        self.existing_token = Token.objects.create(user=self.existing_user)

    # ---------- Original tests ----------

    def test_register_creates_user_and_token(self):
        url = reverse("users:user-create")
        payload = {"username": "newuser", "email": "new@example.com", "password": "pass1234"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "new@example.com")
        self.assertTrue(Token.objects.filter(user=user).exists())
        self.assertNotIn("password", resp.data)

    def test_login_returns_token(self):
        url = reverse("users:login")
        resp = self.client.post(url, {"username": "existing", "password": "password123"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("token", resp.data)
        self.assertEqual(resp.data["token"], self.existing_token.key)

    def test_user_list_requires_authentication_and_returns_list(self):
        url = reverse("users:user-list")
        resp = self.client.get(url, format="json")
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.existing_token.key)
        resp = self.client.get(url, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        usernames = [u.get("username") for u in resp.data]
        self.assertIn("existing", usernames)

    def test_register_duplicate_email_fails(self):
        User.objects.create_user(username="alpha", email="dup@example.com", password="pass1")
        url = reverse("users:user-create")
        payload = {"username": "beta", "email": "dup@example.com", "password": "pass2"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("email" in resp.data or "non_field_errors" in resp.data or "detail" in resp.data)

    # ---------- New edge-case tests ----------

    def test_register_missing_fields_fails(self):
        """
        Registration should fail if required fields are missing.
        """
        url = reverse("users:user-create")
        payloads = [
            {"username": "user1"},  # missing email + password
            {"email": "user@example.com"},  # missing username + password
            {"password": "pass1234"}  # missing username + email
        ]
        for payload in payloads:
            resp = self.client.post(url, payload, format="json")
            self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password_fails(self):
        """
        Login with correct username but wrong password should fail.
        """
        url = reverse("users:login")
        resp = self.client.post(url, {"username": "existing", "password": "wrongpass"}, format="json")
        self.assertIn(resp.status_code, (status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED))

    def test_password_length_validation(self):
        """
        Registration should fail if password is too short (< 8 chars).
        """
        url = reverse("users:user-create")
        payload = {"username": "shortpass", "email": "short@example.com", "password": "123"}
        resp = self.client.post(url, payload, format="json")
        # DRF/Django default UserCreationForm requires 8+ chars
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("password" in resp.data or "non_field_errors" in resp.data)

    def test_register_duplicate_username_fails(self):
        """
        Trying to register with an existing username should fail.
        """
        User.objects.create_user(username="dupuser", email="dup1@example.com", password="pass1234")
        url = reverse("users:user-create")
        payload = {"username": "dupuser", "email": "dup2@example.com", "password": "pass5678"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("username" in resp.data or "non_field_errors" in resp.data)
