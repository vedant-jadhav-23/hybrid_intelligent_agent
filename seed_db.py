import pandas as pd

from database import SessionLocal
from models import Patient, DoctorSchedule


db = SessionLocal()


patients_df = pd.read_csv("patients.csv")

for _, row in patients_df.iterrows():

    patient = Patient(
        patient_id=row["patient_id"],
        first_name=row["first_name"],
        last_name=row["last_name"],
        dob=row["dob"],
        gender=row["gender"],
        phone=row["phone"],
        email=row["email"],
        insurance_company=row["insurance_company"],
        member_id=row["member_id"],
        group_number=row["group_number"]
    )

    db.add(patient)


schedule_df = pd.read_csv("doctors_schedule.csv")

for _, row in schedule_df.iterrows():

    slot = DoctorSchedule(
        doc_id=row["doc_id"],
        doctor_name=row["doctor_name"],
        specialty=row["specialty"],
        day_of_week=row["day_of_week"],
        time_slot=row["time_slot"],
        is_booked=row["is_booked"]
    )

    db.add(slot)


db.commit()
db.close()

print("Database seeded successfully!")