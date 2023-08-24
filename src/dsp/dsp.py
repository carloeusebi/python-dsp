from InquirerPy import prompt

from website.website import Website
from utils import utils, choose_survey

API_URL = "https://www.dellasantapsicologo.it/api"
PATIENTS_ENDPOINT = "patients"
SURVEYS_ENDPOINT = "surveys"

SURVEYS_PARAMS = {"order_by": "last_update", "completed": "1"}
PATIENTS_PARAMS = {"order_by": "lname"}


def get_credentials():
    return prompt(
        [
            {"type": "input", "message": "Username:", "name": "username"},
            {"type": "password", "message": "Password", "name": "password"},
        ]
    )


def main():
    utils.clearscreen()
    website = Website(API_URL)
    # login
    while not website.login(get_credentials()):
        pass
    print("Accesso riuscito")
    # get surveys and patients from website's api
    print("Download in corso... [.........................]", end="\r")
    surveys = website.get(SURVEYS_ENDPOINT, SURVEYS_PARAMS)["list"]
    print("Download in corso... [#############............]", end="\r")
    patients = website.get(PATIENTS_ENDPOINT, PATIENTS_PARAMS)["list"]
    utils.clearscreen()
    # filters completed surveys and add patient's name
    selected_survey = choose_survey.choose_survey(surveys, patients)
    result = website.get("tests/score", params={"token": selected_survey["token"]})[
        "scores"
    ]

    for question in result:
        print(question)
        for variable in result[question]:
            score = result[question][variable]
            print(f"- {variable}: {score}")

    # todo better results handling


if __name__ == "__main__":
    main()
