from InquirerPy.base.control import Choice
from unittest.mock import patch, MagicMock
import unittest

from utils import choose_survey, helpers


class TestChooseSurveyFunctions(unittest.TestCase):
    def setUp(self):
        self.patients = [
            {"id": 1, "fname": "Carlo", "lname": "Eusebi"},
            {"id": 2, "fname": "Susan", "lname": "Brardinelli"},
        ]
        self.surveys = [
            {
                "id": 1,
                "title": "Survey 1",
                "patient_id": 1,
                "patient_name": "Carlo Eusebi",
                "last_update": "2023-07-25",
            },
            {
                "id": 2,
                "title": "Survey 2",
                "patient_id": 2,
                "patient_name": "Susan Brardinelli",
                "last_update": "2023-07-25",
            },
            {
                "id": 3,
                "title": "Survey 3",
                "patient_id": 3,
                "patient_name": "John Doe",
                "last_update": "2023-07-25",
            },
            {
                "id": 4,
                "title": "Survey 4",
                "patient_id": 3,
                "patient_name": "John Doe",
                "last_update": "2023-07-25",
            },
        ]

    def test_get_patient_survey(self):
        result = helpers.get_patient_surveys(1, self.surveys)
        expected_result = [self.surveys[0]]
        # assert one match
        assert result == expected_result
        result = helpers.get_patient_surveys(4, self.surveys)
        # assert no matches
        expected_result = []
        assert result == expected_result
        result = helpers.get_patient_surveys(3, self.surveys)
        expected_result = [
            self.surveys[2],
            self.surveys[3],
        ]
        # assert more than one match
        assert result == expected_result

    def test_get_patient_name(self):
        result = helpers.get_patient_name(1, self.patients)
        expected_result = "Carlo Eusebi"
        assert result == expected_result
        result = helpers.get_patient_name(3, self.patients)
        expected_result = None
        assert result == expected_result

    def test_get_patients_choices(self):
        choices = choose_survey.get_patients_choices(self.patients)
        expected_choices = [
            Choice(1, name="Eusebi Carlo"),
            Choice(2, name="Brardinelli Susan"),
        ]
        assert choices == expected_choices

    def test_get_surveys_choices(self):
        choices = choose_survey.get_surveys_choices(self.surveys)
        expected_choices = [
            Choice(1, name="Survey 1 di Carlo Eusebi completato il 2023-07-25"),
            Choice(2, name="Survey 2 di Susan Brardinelli completato il 2023-07-25"),
            Choice(3, name="Survey 3 di John Doe completato il 2023-07-25"),
            Choice(4, name="Survey 4 di John Doe completato il 2023-07-25"),
        ]
        assert choices == expected_choices

    def test_get_surveys_by_id(self):
        selected_survey = helpers.get_survey_by_id(1, self.surveys)
        assert selected_survey == self.surveys[0]
        # test choosing back (-1) returns None
        selected_survey = helpers.get_survey_by_id(-1, self.surveys)
        assert selected_survey is None

    @patch("utils.choose_survey.prompt", return_value=[1])
    def test_choose_between_surveys(self, mocked_prompt):
        result = choose_survey.choose_between_surveys(self.surveys)
        self.assertEqual(result, 1)

    @patch("utils.choose_survey.prompt", return_value=[1])
    def test_choose_between_patients(self, mocked_prompt):
        result = choose_survey.choose_between_patients(self.patients)
        self.assertEqual(result, 1)

    # Test scenario when a surveys is selected
    # Simulate user input: "Test" -> Choose survey ID 2
    @patch("utils.choose_survey.prompt", return_value=[1])
    @patch("utils.choose_survey.choose_between_surveys", return_value=2)
    def test_choose_survey_for_survey(self, mocked_prompt, mocked_func):
        expected_survey = self.surveys[1]  # survey with ID 2
        actual_survey = choose_survey.choose_survey(self.surveys, self.patients)
        self.assertEqual(expected_survey, actual_survey)

    # Test scenario when a patient with completed surveys is selected
    # Simulated user input "Pazienti" -> Choose patient ID 2 -> Choose survey ID 2
    @patch("utils.choose_survey.prompt", return_value=[0])
    @patch("utils.choose_survey.choose_between_patients", return_value=2)
    @patch("utils.choose_survey.choose_between_surveys", return_value=2)
    def test_choose_survey_for_patient_with_completed_surveys(self, m1, m2, m3):
        expected_survey = self.surveys[1]  # survey with ID 1
        actual_survey = choose_survey.choose_survey(self.surveys, self.patients)
        self.assertEqual(expected_survey, actual_survey)

    # Test scenario when a patient with no completed surveys is selected
    # Simulate user input "Pazienti" -> Choose patient ID 1 -> Choose survey ID 1
    @patch("utils.choose_survey.prompt", return_value=[0])
    @patch("utils.choose_survey.choose_between_patients", return_value=4)
    @patch("utils.choose_survey.utils.test_passed", side_effect=[False, True])
    @patch("utils.choose_survey.utils.clearscreen")
    def test_choose_survey_for_patient_with_existing_surveys(self, m1, m2, m3, m4):
        patients_with_no_surveys = [{"id": 4, "fname": "John", "lname": "Doe"}]
        expected_message = "John Doe non ha completato nessun Test"
        with patch("builtins.print") as mock_print:
            choose_survey.choose_survey(self.surveys, patients_with_no_surveys)
            mock_print.assert_called_once_with(expected_message)

    # Simulate user input: "Esci" to exit
    @patch("utils.choose_survey.prompt", return_value=[2])
    def test_choose_survey_exit_option(self, mocked_prompt):
        with self.assertRaises(SystemExit) as context:
            choose_survey.choose_survey(self.surveys, self.patients)
        self.assertEqual(context.exception.code, 0)

    # Simulate user input: "Pazienti" -> ">Indietro" to go back -> "Esci" to exit
    @patch("utils.choose_survey.prompt", side_effect=[[0], [2]])
    @patch("utils.choose_survey.choose_between_patients", return_value=-1)
    @patch("utils.choose_survey.utils.clearscreen")
    def test_choose_survey_patients_then_back_option(self, m1, m2, m3):
        with self.assertRaises(SystemExit) as context:
            choose_survey.choose_survey(self.surveys, self.patients)
        self.assertEqual(context.exception.code, 0)

    # Simulate user input: "Test" -> ">Indietro" to go back -> "Esci" to exit
    @patch("utils.choose_survey.prompt", side_effect=[[1], [2]])
    @patch("utils.choose_survey.choose_between_surveys", return_value=-1)
    @patch("utils.choose_survey.utils.clearscreen")
    def test_choose_survey_surveys_then_back_option(self, m1, m2, m3):
        with self.assertRaises(SystemExit) as context:
            choose_survey.choose_survey(self.surveys, self.patients)
        self.assertEqual(context.exception.code, 0)

    # Simulate user input: "Pazienti" -> ID 1 -> ">Indietro" to go back -> "Esci" to exit
    @patch("utils.choose_survey.prompt", side_effect=[[0], [2]])
    @patch("utils.choose_survey.choose_between_patients", return_value=1)
    @patch("utils.choose_survey.choose_between_surveys", return_value=-1)
    @patch("utils.choose_survey.utils.clearscreen")
    def test_choose_survey_patients_then_surveys_then_back_option(self, m1, m2, m3, m4):
        with self.assertRaises(SystemExit) as context:
            choose_survey.choose_survey(self.surveys, self.patients)
        self.assertEqual(context.exception.code, 0)
