from faker import Faker
import pandas as pd
import random

fake = Faker()

patients = []

for i in range(50):
    patient = {
        "patient_id": f"P{i+1}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "dob": fake.date_of_birth(
            minimum_age=18,
            maximum_age=80
        ).strftime("%m/%d/%Y"),
        "gender": random.choice(["Male", "Female"]),
        "phone": fake.phone_number(),
        "email": fake.email(),
        "insurance_company": random.choice(
            ["Star Health", "HDFC ERGO", "ICICI Lombard"]
        ),
        "member_id": fake.bothify("??#####"),
        "group_number": fake.bothify("GRP###")
    }

    patients.append(patient)


patients_df = pd.DataFrame(patients)

patients_df.to_csv(
    "patients.csv",
    index=False
)


doctor_info = [
    ("D1", "Dr Patel", "Physio"),
    ("D2", "Dr Oza", "Cardiology"),
    ("D3", "Dr Kejriwal", "Dermatology")
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

slots = [
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "15:00"
]

doctor_schedule = []

for doc_id, doctor_name, specialty in doctor_info:

    for day in days:

        for slot in slots:

            doctor_schedule.append({
                "doc_id": doc_id,
                "doctor_name": doctor_name,
                "specialty": specialty,
                "day_of_week": day,
                "time_slot": slot,
                "is_booked": False
            })


schedule_df = pd.DataFrame(doctor_schedule)

schedule_df.to_csv(
    "doctors_schedule.csv",
    index=False
)