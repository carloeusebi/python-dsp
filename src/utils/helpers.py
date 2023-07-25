def get_patient_surveys(patient_id: int, surveys: list[dict]):
    patient_surveys: list[dict] = []
    for survey in surveys:
        if patient_id == survey["patient_id"]:
            patient_surveys.append(survey)
    return patient_surveys


def get_survey_by_id(survey_id: int, surveys: list[dict]) -> dict:
    return next((s for s in surveys if s["id"] == survey_id), None)


def get_patient_name(patient_id: int, patients: list[dict]) -> str:
    patient = next((p for p in patients if p["id"] == patient_id), None)
    return f"{patient['fname']} {patient['lname']}" if patient is not None else None
