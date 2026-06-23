from pydantic import BaseModel


class PatientLookup(BaseModel):
    first_name: str
    last_name: str
    dob: str


class DoctorAvailability(BaseModel):
    specialty: str
    day: str
    duration_minutes: int


class AppointmentBook(BaseModel):
    patient_id: str
    doc_id: str
    day: str
    time_slot: str