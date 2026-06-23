from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from database import Base


class Patient(Base):

    __tablename__ = "patients"

    patient_id = Column(String, primary_key=True)

    first_name = Column(String)

    last_name = Column(String)

    dob = Column(String)

    gender = Column(String)

    phone = Column(String)

    email = Column(String)

    insurance_company = Column(String)

    member_id = Column(String)

    group_number = Column(String)



class DoctorSchedule(Base):

    __tablename__ = "doctor_schedule"

    id = Column(Integer, primary_key=True, autoincrement=True)

    doc_id = Column(String)

    doctor_name = Column(String)

    specialty = Column(String)

    day_of_week = Column(String)

    time_slot = Column(String)

    is_booked = Column(Boolean)



class Appointment(Base):

    __tablename__ = "appointments"

    appointment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patient_id = Column(
        String,
        ForeignKey("patients.patient_id")
    )

    doc_id = Column(String)

    day_of_week = Column(String)

    time_slot = Column(String)