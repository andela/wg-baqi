# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import logging
from django.contrib.auth.models import User
from django.urls import reverse
from wger.core.models import UserProfile
from wger.core.forms import RegistrationForm
from wger.core.forms import RegistrationFormNoCaptcha
from wger.core.tests.base_testcase import WorkoutManagerTestCase

logger = logging.getLogger(__name__)


class RegistrationTestCase(WorkoutManagerTestCase):
    '''
    Tests registering a new user
    '''

    def test_registration_captcha(self):
        '''
        Tests that the correct form is used depending on global
        configuration settings
        '''
        with self.settings(WGER_SETTINGS={'USE_RECAPTCHA': True,
                                          'REMOVE_WHITESPACE': False,
                                          'ALLOW_REGISTRATION': True,
                                          'ALLOW_GUEST_USERS': True,
                                          'TWITTER': False}):
            response = self.client.get(reverse('core:user:registration'))
            self.assertIsInstance(response.context['form'], RegistrationForm)

        with self.settings(WGER_SETTINGS={'USE_RECAPTCHA': False,
                                          'REMOVE_WHITESPACE': False,
                                          'ALLOW_REGISTRATION': True,
                                          'ALLOW_GUEST_USERS': True,
                                          'TWITTER': False}):
            response = self.client.get(reverse('core:user:registration'))
            self.assertIsInstance(
                response.context['form'], RegistrationFormNoCaptcha)

    def test_register(self):

        # Fetch the registration page
        response = self.client.get(reverse('core:user:registration'))
        self.assertEqual(response.status_code, 200)

        # Fill in the registration form
        registration_data = {'username': 'myusername',
                             'password1': 'secret',
                             'password2': 'secret',
                             'email': 'not an email',
                             'g-recaptcha-response': 'PASSED', }
        count_before = User.objects.count()

        # Wrong email
        response = self.client.post(
            reverse('core:user:registration'), registration_data)
        self.assertFalse(response.context['form'].is_valid())
        self.user_logout()

        # Correct email
        registration_data['email'] = 'my.email@example.com'
        response = self.client.post(
            reverse('core:user:registration'), registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_before + 1, count_after)
        self.user_logout()

        # Username already exists
        response = self.client.post(
            reverse('core:user:registration'), registration_data)
        count_after = User.objects.count()
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_before + 1, count_after)

        # Email already exists
        registration_data['username'] = 'my.other.username'
        response = self.client.post(
            reverse('core:user:registration'), registration_data)
        count_after = User.objects.count()
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_before + 1, count_after)

    def test_registration_deactivated(self):
        '''
        Test that with deactivated registration no users can register
        '''

        with self.settings(WGER_SETTINGS={'USE_RECAPTCHA': False,
                                          'REMOVE_WHITESPACE': False,
                                          'ALLOW_GUEST_USERS': True,
                                          'ALLOW_REGISTRATION': False}):

            # Fetch the registration page
            response = self.client.get(reverse('core:user:registration'))
            self.assertEqual(response.status_code, 302)

            # Fill in the registration form
            registration_data = {'username': 'myusername',
                                 'password1': 'secret',
                                 'password2': 'secret',
                                 'email': 'my.email@example.com',
                                 'g-recaptcha-response': 'PASSED', }
            count_before = User.objects.count()

            response = self.client.post(
                reverse('core:user:registration'), registration_data)
            count_after = User.objects.count()
            self.assertEqual(response.status_code, 302)
            self.assertEqual(count_before, count_after)


class RegistrationTestCaseRest(WorkoutManagerTestCase):

    def test_register(self):
        url = '/api/v2/signup/'
        unauthorized = dict(username='test_user1', email='test1@gmail.com',
                            password='pAss!w@rd')
        # Test unauthorized user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Test register via Rest API
        self.user_login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        test_data = dict(username='test_user', email='test@gmail.com',
                         password='pAss!w@rd')
        response = self.client.post(url, data=test_data)
        self.assertEqual(response.status_code, 201)

        # Test username exists
        response1 = self.client.post(url, data=test_data)
        self.assertEqual(response1.status_code, 400)

        # test no data
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 400)

        # test get user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test authorized user
        user = User.objects.get(username="test")
        userprofile = UserProfile.objects.get(user=user)
        userprofile.create_user_via_api = False
        userprofile.save()
        create_user = {"username": "testperms", "password": "adminuser",
                       "email": "email@test.com"}
        response = self.client.post(url, data=create_user)
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_user(self):
        ''' Test unauthorized user '''

        url = '/api/v2/signup/'
        unauthorized = dict(username='test_user1', email='test1@gmail.com',
                            password='pAss!w@rd')
        response = self.client.post(url, data=unauthorized)
        self.assertEqual(response.status_code, 403)

    def test_get_all_created_users(self):
        """
        test get all users
        """
        url = '/api/v2/signup/'
        self.user_login()
        response = self.client.get(url)
        User.objects.all()
        self.assertEqual(response.status_code, 200)
