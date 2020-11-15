"""
This file generates sample data in the database

:author William Boyles:
"""
from datetime import datetime, timedelta

from .persistent import db

from ..enums.user_role.user_role import UserRole
from ..enums.state.state import State
from ..enums.drug_type.drug_type import DrugType
from ..enums.blood_type.blood_type import BloodType
from ..enums.ethnicity.ethnicity import Ethnicity
from ..enums.gender.gender import Gender

from .user.user import User
from .user.patient.patient import Patient
from .institution.pharmacy.pharmacy import Pharmacy
from .institution.hospital.hospital import Hospital
from .user.personnel.personnel import Personnel
from .prescription.prescription import Prescription

from .drug.drug import Drug

# Password used when generating sample users
DEFAULT_PASSWORD = "password"


def generate_sample_data():
    """
    Drop exiting tables, recreate them, and generate sample data
    """

    db.drop_all()
    db.create_all()

    _generate_sample_users()
    _generate_pharmacy()
    _generate_hospital()
    _generate_drugs()
    _generate_patient()
    _generate_personnel()
    _generate_prescription()


def _generate_sample_users():
    """
    Generate some sample users. One per user role.
    Username will be their role name and password will be default.
    """

    for role in UserRole:
        user = User()
        user.username = role.value
        user.role = role
        user.set_password(DEFAULT_PASSWORD)

        db.session.add(user)

    db.session.commit()


def _generate_patient():
    """
    For the user 'patient' we generated previously, fill out the basic demographics, creating a patient object
    """

    with db.session.no_autoflush:
        user = User.query.filter(User.username == UserRole.PATIENT.value).first()
        patient = Patient()
        patient.first_name = "Some"
        patient.last_name = "Patient"
        patient.dob = datetime(day=29, month=2, year=2000)
        patient.address = "123 Patient St."
        patient.city = "Everytown"
        patient.state = State.NORTH_CAROLINA
        patient.zip = 12345
        patient.email = "some_patient@email.com"
        patient.gender = Gender.Male
        patient.ethnicity = Ethnicity.White
        patient.drug_type = DrugType.Generic
        patient.blood_type = BloodType.ONeg
        patient.pharmacy = Pharmacy.query.first()
        patient.user = user

    db.session.add(patient)

    db.session.commit()


def _generate_personnel():
    """
    Generate hcp and pharmacist personnel
    """

    with db.session.no_autoflush:
        hcp = User.query.filter(User.username == UserRole.HCP.value).first()
        hospital = Hospital.query.first()
        hcp_personnel = Personnel()
        hcp_personnel.first_name = "Some"
        hcp_personnel.last_name = "HCP"
        hcp_personnel.address = "123 HCP St."
        hcp_personnel.city = "Everytown"
        hcp_personnel.state = State.NORTH_CAROLINA
        hcp_personnel.zip = 12345
        hcp_personnel.hospital = hospital
        hcp_personnel.user = hcp

        pharmacist = User.query.filter(
            User.username == UserRole.PHARMACIST.value
        ).first()
        pharmacy = Pharmacy.query.first()
        pharmacist_personnel = Personnel()
        pharmacist_personnel.first_name = "Some"
        pharmacist_personnel.last_name = "Pharmacist"
        pharmacist_personnel.address = "123 Pharmacist St."
        pharmacist_personnel.city = "Everytown"
        pharmacist_personnel.state = State.NORTH_CAROLINA
        pharmacist_personnel.zip = 12345
        pharmacist_personnel.pharmacy = pharmacy
        pharmacist_personnel.user = pharmacist

    db.session.add(hcp_personnel)
    db.session.add(pharmacist_personnel)
    db.session.commit()


def _generate_pharmacy():
    """
    Generate a pharmacy
    """

    p = Pharmacy()
    p.name = "pharmacy"
    p.address = "123 Pharmacy St"
    p.city = "Everytown"
    p.state = State.NORTH_CAROLINA
    p.zip = 12345

    db.session.add(p)
    db.session.commit()


def _generate_hospital():
    """
    Generate a hospital
    """

    h = Hospital()
    h.name = "hospital"
    h.address = "123 Hospital St"
    h.city = "Everytown"
    h.state = State.NORTH_CAROLINA
    h.zip = 12345

    db.session.add(h)
    db.session.commit()


def _generate_drugs():
    """
    Generate a generic and branded type of a drug
    """

    dgn = Drug()
    dgn.name = "GeneraDrug"
    dgn.type = DrugType.Generic
    dgn.code = "1234-5678-90"
    dgn.description = "A generic drug"

    dbr = Drug()
    dbr.name = "BranDrug"
    dbr.type = DrugType.Brand
    dbr.code = "1234-5678-90"
    dbr.description = "A brand drug"

    db.session.add(dgn)
    db.session.add(dbr)
    db.session.commit()


def _generate_prescription():
    """
    Generate a prescription for the patient
    """

    with db.session.no_autoflush:
        patient = Patient.query.first()
        hcp = Personnel.query.filter(Personnel.hospital != None).first()
        pharmacy = Pharmacy.query.first()
        drug = Drug.query.first()

        prescription = Prescription()
        prescription.patient = patient
        prescription.pharmacy = pharmacy
        prescription.dosage = 100
        prescription.prescriber = hcp
        prescription.drug = drug
        prescription.start_date = datetime.today()
        prescription.end_date = prescription.start_date + timedelta(weeks=3)
        prescription.renewals = 1

    db.session.add(prescription)
    db.session.commit()
