from InquirerPy import prompt

from website.website import Website
from utils import utils, choose_survey

API_URL = "https://www.carloeusebiwebdeveloper.it/api"
PATIENTS_ENDPOINT = "patients"
SURVEYS_ENDPOINT = "surveys"
PATIENTS_ORDER = "lname"
SURVEYS_ORDER = "last_updated"


def get_credentials():
    return prompt(
        [
            {"type": "input", "message": "Username:", "name": "username"},
            {"type": "password", "message": "Password", "name": "password"},
        ]
    )


def map_surveys(surveys: list[dict], patients: list[dict]) -> list[dict]:
    completed_surveys: list[dict] = []
    for survey in surveys:
        patient_id = survey["patient_id"]
        for patient in patients:
            if patient["id"] == patient_id:
                survey["patient_name"] = f"{patient['fname']} {patient['lname']}"
        if survey["completed"]:
            completed_surveys.append(survey)
    return completed_surveys


def main():
    utils.clearscreen()
    website = Website(API_URL)
    # login
    while not website.login(get_credentials()):
        pass
    print("Accesso riuscito")
    # get surveys and patients from website's api
    print("Download in corso... [-------------------------]", end="\r")
    row_surveys = website.get(SURVEYS_ENDPOINT, SURVEYS_ORDER)
    print("Download in corso... [=============------------]", end="\r")
    patients = website.get(PATIENTS_ENDPOINT, PATIENTS_ORDER)
    utils.clearscreen()
    # filters completed surveys and add patient's name
    surveys = map_surveys(row_surveys, patients)
    selected_survey = choose_survey.choose_survey(surveys, patients)
    print(selected_survey)


if __name__ == "__main__":
    main()
