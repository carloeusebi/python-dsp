from InquirerPy import inquirer, prompt
from InquirerPy.base.control import Choice

from utils import utils


def get_patient_surveys(patient_id: int, surveys: list[dict]):
    patient_surveys: list[dict] = []
    for survey in surveys:
        if patient_id == survey["patient_id"]:
            patient_surveys.append(survey)
    return patient_surveys


def get_patient_name(patient_id: int, patients: list[dict]) -> str:
    patient = next(p for p in patients if p["id"] == patient_id)
    return f"{patient['fname']} {patient['lname']}"


def create_patients_choices(patients: list[dict]) -> list[Choice]:
    return [Choice(p["id"], name=f"{p['lname']} {p['fname']}") for p in patients]


def create_surveys_choices(surveys: list[dict]) -> list[Choice]:
    return [
        Choice(
            s["id"],
            name=f"{s['title']} di {s['patient_name']} completato il {s['last_update']}",
        )
        for s in surveys
    ]


def choose_between_patients(patients: list[dict]) -> dict:
    choices = create_patients_choices(patients)
    return inquirer.fuzzy(
        message="Scegli un Paziente:",
        choices=[{"value": -1, "name": ">Indietro"}, *choices],
        pointer=">>",
        height=10,
    ).execute()


def choose_between_surveys(surveys: list[dict]) -> dict:
    choices = create_surveys_choices(surveys)
    return inquirer.fuzzy(
        message="Scegli un Test:",
        choices=[{"value": -1, "name": ">Indietro"}, *choices],
        pointer=">>",
        height=10,
    ).execute()


def choose_survey(surveys: list[dict], patients: list[dict]) -> dict:
    """
    This function allows the user to choose a survey from a list of completed surveys for a specific patient
    or from a list of all available surveys. The function presents a fuzzy search interface where the user can
    select between patients, surveys, or choose to exit the program.

    Parameters:
        surveys (list[dict]): A list of dictionaries representing completed surveys.
            Each dictionary should contain information about a completed survey.
        patients (list[dict]): A list of dictionaries representing patients.
            Each dictionary should contain information about a patient.

    Returns:
        dict: A dictionary representing the selected survey.

    Usage:
        - If the user selects "Pazienti" (Patients), the function will prompt the user to choose a patient.
          Then, it will display the completed surveys for the selected patient. The user can choose one of
          the completed surveys from the list.
        - If the selected patient has no completed surveys, a message will be displayed, and the user will
          be prompted to choose a different option.
        - If the user selects "Test" (Surveys), the function will display all available surveys, and the user
          can choose one of them from the list.
        - The user can also select "Esci" (Exit) to terminate the program.
    """
    while True:
        answer = prompt(
            {
                "type": "fuzzy",
                "message": "Cerca tra:",
                "choices": ["Pazienti", "Test", "Esci"],
                "pointer": ">>",
            }
        )[0]
        if answer == "Pazienti":
            selected_patient_id = choose_between_patients(patients)
            # if answer is 'go back' continue
            if selected_patient_id == -1:
                utils.clearscreen()
                continue
            # search through the completed surveys of the selected patient
            selected_patients_surveys = get_patient_surveys(
                int(selected_patient_id), surveys
            )
            # if the patient doesn't have completed surveys prints a message and repeat the cycle
            if not selected_patients_surveys:
                utils.clearscreen()
                patient_name = get_patient_name(selected_patient_id, patients)
                print(f"{patient_name} non ha completato nessun Test")
            else:
                # give the selected patients surveys as options
                selected_survey = choose_between_surveys(selected_patients_surveys)
                # if answer is 'go back' continue
                if selected_survey == -1:
                    utils.clearscreen()
                    continue
                return selected_survey
        elif answer == "Test":
            selected_survey = choose_between_surveys(surveys)
            # if answer is 'go back' continue
            if selected_survey == -1:
                utils.clearscreen()
                continue
            return selected_survey
        elif answer == "Esci":
            exit()