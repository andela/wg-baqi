"""Test social auth login/signup and default login."""
from rest_framework import status
from .base_testcase import WorkoutManagerTestCase

SOCIAL_URL = '/social/auth-login/'


class TestSocialLogin(WorkoutManagerTestCase):
    """.Class to test Social Login."""

    def test_successful_login_with_twitter(self):
        """Test successful login with twitter."""
        res = self.client.post(SOCIAL_URL, self.twitter_user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('username'), "dev_trevor")

    def test_invalid_provider(self):
        """Test unsupported social provider."""
        res = self.client.post(SOCIAL_URL, self.unsupported_provider)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'],
                         "Provider invalid or not supported")

    def test_invalid_access_token(self):
        """Test invalid access token."""
        res = self.client.post(SOCIAL_URL, self.invalid_access_token)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data.get('error'), "Invalid credentials")

    def test_invalid_secret_token(self):
        """Test invalid secret token."""
        res = self.client.post(SOCIAL_URL, self.invalid_secret_token)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data.get('error'), "Invalid credentials")

    def test_missing_access_token_field(self):
        """Test missing access token."""
        res = self.client.post(SOCIAL_URL, self.missing_access_field)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_provider_token_field(self):
        """Test missing provider field."""
        res = self.client.post(SOCIAL_URL, self.missing_provider_field)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_secret_token_field(self):
        """Test missing twitter secret token."""
        res = self.client.post(SOCIAL_URL, self.missing_twitter_secret_field)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_token_field_access(self):
        """Test empty access token."""
        res = self.client.post(SOCIAL_URL, self.missing_token_access)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_secret_field_access(self):
        """Test empty secret token."""
        res = self.client.post(SOCIAL_URL, self.missing_token_secret)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_provider_field_access(self):
        """Test empty secret token."""
        res = self.client.post(SOCIAL_URL, self.missing_provider)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data.get('non_field_errors'),
                         ["A provider is required for Social Login"])
