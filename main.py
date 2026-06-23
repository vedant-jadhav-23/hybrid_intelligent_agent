from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Patient, DoctorSchedule, Appointment
from schemas import (
    PatientLookup,
    DoctorAvailability,
    AppointmentBook
)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/patients/lookup")
def lookup_patient(
    body: PatientLookup,
    db: Session = Depends(get_db)
):

    patient = db.query(Patient).filter(
        Patient.first_name == body.first_name,
        Patient.last_name == body.last_name,
        Patient.dob == body.dob
    ).first()

    if patient:
        return {
            "status": "returning",
            "patient_id": patient.patient_id
        }

    return {
        "status": "new",
        "patient_id": None
    }


@app.post("/doctors/availability")
def doctor_availability(
    body: DoctorAvailability,
    db: Session = Depends(get_db)
):

    schedule = db.query(DoctorSchedule).filter(
        DoctorSchedule.specialty == body.specialty,
        DoctorSchedule.day_of_week == body.day,
        DoctorSchedule.is_booked == False
    ).all()

    available = []

    for slot in schedule:

        available.append({

            "doc_id": slot.doc_id,

            "doctor_name": slot.doctor_name,

            "specialty": slot.specialty,

            "time_slot": slot.time_slot

        })

    return available


@app.post("/appointments/book")
def book_appointment(
    body: AppointmentBook,
    db: Session = Depends(get_db)
):

    slot = db.query(DoctorSchedule).filter(
        DoctorSchedule.doc_id == body.doc_id,
        DoctorSchedule.day_of_week == body.day,
        DoctorSchedule.time_slot == body.time_slot
    ).first()

    if slot is None:
        return {
            "message": "Slot not found"
        }

    if slot.is_booked:
        return {
            "message": "Slot already booked"
        }

    slot.is_booked = True

    appointment = Appointment(
        patient_id=body.patient_id,
        doc_id=body.doc_id,
        day_of_week=body.day,
        time_slot=body.time_slot
    )

    db.add(appointment)
    db.commit()

    return {
        "message": "Appointment booked successfully"
    }