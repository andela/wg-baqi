from wger.core.tests.base_testcase import (
    BaseTestCase,
)
from wger.core.tests.api_base_test import ApiBaseTestCase
from rest_framework import status
from django.contrib.auth.models import User
from wger.core.models import UserProfile

register_url = "/api/v2/signup/"


class APIUserRegistrationTestCase(ApiBaseTestCase):
    """ Tests user registration throught the api """
    fixtures = BaseTestCase.fixtures
    full_user = {"username": "apiTest",
                 "email": "test@gmail.com",
                 "password": "testpass"}

    def register_user(self, user=None, ex_status=status.HTTP_201_CREATED):
        """ Helper function for register user"""
        if not user:
            user = self.full_user
        url = register_url
        response = self.client.post(url, user)
        if ex_status == status.HTTP_201_CREATED:
            self.assertEqual(response.status_code, ex_status)

        else:
            self.assertEqual(response.status_code, ex_status)
        return response

    def test_admin_api_user_create(self):
        """ Test that an admin can create user through the api """

        expected_message = 'User was successfully created'
        self.get_credentials(username='admin')
        response = self.register_user()
        message = response.data['message']
        self.assertEqual(expected_message, message)
        self.assertEqual(response.status_code, 201)

    def test_normal_user_cannot_create_user(self):
        """ Test unauthirized user """
        self.register_user(None, 403)

    def test_normal_user_with_permission_can_create_user(self):
        user = User.objects.get(username="admin")
        userprofile = UserProfile.objects.get(user=user)
        userprofile.user_can_create_users = True
        userprofile.save()
        create_user = {"username": "testperms",
                       "email": "test@gmail.com",
                       "password": "adminuser"}
        self.get_credentials(username='admin')
        self.register_user(user=create_user)

    def test_register_with_missing_password(self):
        create_user = {"username": "testperms"}
        self.get_credentials(username='admin')
        self.register_user(create_user, status.HTTP_400_BAD_REQUEST)

    def test_register_with_missing_username(self):
        create_user = {"password": "testperms"}
        self.get_credentials("admin")
        self.register_user(create_user, status.HTTP_400_BAD_REQUEST)

        self.get_credentials("admin")

    def test_register_with_missing_email(self):
        create_user = {"password": "passhere3"}
        self.get_credentials(username='admin')
        self.register_user(create_user, status.HTTP_400_BAD_REQUEST)


class ApiAssignCreateRoleTestcase(APIUserRegistrationTestCase):
    """Testcase for assigning user create user Permission"""

    fixtures = BaseTestCase.fixtures

    def assign_create_user_role(self, ex_status=status.HTTP_201_CREATED):
        url = "/api/v2/signup/"
        data = {'username': 'test'}

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, ex_status)

    def test_assign_create_user_permission_without_data(self):
        url = "/api/v2/signup/"
        data = {}
        self.get_credentials("admin")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
