from wger.core.tests.api_base_test import (ApiGetTestCase, ApiBaseTestCase)
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.exercises.models import Exercise
from rest_framework.test import APITestCase
from rest_framework import status


class TestExerciseInfo(
        ApiBaseTestCase, ApiGetTestCase, WorkoutManagerTestCase):
    """
    Define test variables for get exercise by id
    """

    pk = 1
    resource = Exercise
    private_resource = False


class CustomBaseTestCase(APITestCase):
    """
    Test variable definitions
    """

    api_version = "v2"
    resource = None
    pk = None
    private_resource = True

    def get_resource_name(self):
        """
        Returns the name of the resource in lowercase
        """

        return self.resource.__name__.lower()

    @property
    def url(self):
        """
        Return the URL to use for testing
        """

        return "/api/{0}/{1}/".format(
            self.api_version, self.get_resource_name())


class CustomApiGetTestCase(object):
    """
    Base test case for testing GET access to the API
    """

    def test_get_overview(self):
        """
        Test accessing the overview view of a resource
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAllExerciseInfo(
        CustomBaseTestCase, CustomApiGetTestCase, WorkoutManagerTestCase):
    """
    Define test variables for geting all exercises
    """

    resource = Exercise
    private_resource = False
