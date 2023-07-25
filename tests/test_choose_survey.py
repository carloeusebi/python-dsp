from utils import choose_survey, helpers

from InquirerPy.base.control import Choice


def get_dummy_patients() -> list[dict]:
    return [
        {"id": 1, "fname": "Carlo", "lname": "Eusebi"},
        {"id": 2, "fname": "Susan", "lname": "Brardinelli"},
    ]


def get_dummy_surveys() -> list[dict]:
    return [
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


def test_get_patient_survey():
    surveys = get_dummy_surveys()
    result = helpers.get_patient_surveys(1, surveys)
    expected_result = [surveys[0]]
    # assert one match
    assert result == expected_result
    result = helpers.get_patient_surveys(4, surveys)
    # assert no matches
    expected_result = []
    assert result == expected_result
    result = helpers.get_patient_surveys(3, surveys)
    expected_result = [
        surveys[2],
        surveys[3],
    ]
    # assert more than one match
    assert result == expected_result


def test_get_patient_name():
    patients = get_dummy_patients()
    result = helpers.get_patient_name(1, patients)
    expected_result = "Carlo Eusebi"
    assert result == expected_result
    result = helpers.get_patient_name(3, patients)
    expected_result = None
    assert result == expected_result


def test_get_patients_choices():
    patients = get_dummy_patients()
    choices = choose_survey.get_patients_choices(patients)
    expected_choices = [
        Choice(1, name="Eusebi Carlo"),
        Choice(2, name="Brardinelli Susan"),
    ]
    assert choices == expected_choices


def test_get_surveys_choices():
    surveys = get_dummy_surveys()
    choices = choose_survey.get_surveys_choices(surveys)
    expected_choices = [
        Choice(1, name="Survey 1 di Carlo Eusebi completato il 2023-07-25"),
        Choice(2, name="Survey 2 di Susan Brardinelli completato il 2023-07-25"),
        Choice(3, name="Survey 3 di John Doe completato il 2023-07-25"),
        Choice(4, name="Survey 4 di John Doe completato il 2023-07-25"),
    ]
    assert choices == expected_choices


def test_get_surveys_by_id():
    surveys = get_dummy_surveys()
    selected_survey = helpers.get_survey_by_id(1, surveys)
    assert selected_survey == surveys[0]
    # test choosing back (-1) returns None
    selected_survey = helpers.get_survey_by_id(-1, surveys)
    assert selected_survey is None
