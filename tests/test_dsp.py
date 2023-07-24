import unittest
from unittest.mock import patch

from dsp.dsp import get_credentials, map_surveys


class TestDsp(unittest.TestCase):
    @patch("dsp.dsp.prompt")
    def test_get_credentials(self, mocked_prompt):
        mocked_prompt.return_value = {"username": "test_user", "password": "test_pass"}
        result = get_credentials()
        self.assertIsInstance(result, dict)
        self.assertIn("username", result)
        self.assertIn("password", result)
        self.assertEqual(result["username"], "test_user")
        self.assertEqual(result["password"], "test_pass")

    def test_map_surveys(self):
        surveys = [
            {"id": 1, "title": "Survey 1", "patient_id": 1, "completed": True},
            {"id": 2, "title": "Survey 2", "patient_id": 2, "completed": False},
            {"id": 3, "title": "Survey 3", "patient_id": 3, "completed": True},
        ]
        patients = [
            {"id": 1, "fname": "Carlo", "lname": "Eusebi"},
            {"id": 2, "fname": "Susan", "lname": "Brardinelli"},
            {"id": 3, "fname": "Ares", "lname": "Mallucci"},
        ]
        expected_result = [
            {
                "id": 1,
                "title": "Survey 1",
                "patient_id": 1,
                "completed": True,
                "patient_name": "Carlo Eusebi",
            },
            {
                "id": 3,
                "title": "Survey 3",
                "patient_id": 3,
                "completed": True,
                "patient_name": "Ares Mallucci",
            },
        ]
        mapped_surveys = map_surveys(surveys, patients)
        assert mapped_surveys == expected_result
