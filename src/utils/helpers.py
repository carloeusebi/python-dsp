from InquirerPy import inquirer
from InquirerPy.base.control import Choice


def get_patient_surveys(patient_id: int, surveys: list[dict]):
    patient_surveys: list[dict] = []
    for survey in surveys:
        if patient_id == survey["patient_id"]:
            patient_surveys.append(survey)
    return patient_surveys


def create_patients_choices(patients: list[dict[str, int | str]]) -> list[Choice]:
    return [Choice(p["id"], name=f"{p['lname']} {p['fname']}") for p in patients]


def create_surveys_choices(surveys: list[dict[str, int | str]]) -> list[Choice]:
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
