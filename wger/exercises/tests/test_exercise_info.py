from wger.core.tests.api_base_test import (ApiGetTestCase, ApiBaseTestCase)
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.exercises.models import Exercise
from rest_framework.test import APITestCase
from rest_framework import status


class TestExerciseInfo(
        ApiBaseTestCase, ApiGetTestCase, WorkoutManagerTestCase):

    pk = 1
    resource = Exercise
    private_resource = False


class CustomBaseTestCase(APITestCase):
    api_version = "v2"
    """
    The current API version to test
    """

    resource = None
    """
    The current resource to be tested (Model class)
    """

    pk = None
    """
    The pk of the detail view to test
    """

    private_resource = True
    """
    A flag indicating whether the resource can be updated (POST, PATCH)
    by the owning user (workout, etc.)
    """

    def get_resource_name(self):
        """
        Returns the name of the resource. The default is the name of the model
        class used in lower letters
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

    resource = Exercise
    private_resource = False
