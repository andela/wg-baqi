from wger.core.tests.api_base_test import (ApiGetTestCase, ApiBaseTestCase)
from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.exercises.models import Exercise


class TestExerciseInfo(ApiBaseTestCase, ApiGetTestCase, WorkoutManagerTestCase):


    pk = 1
    resource = Exercise
    private_resource = False