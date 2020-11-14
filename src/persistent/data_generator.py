"""
This file generates sample data in the database

:author William Boyles:
"""

from .persistent import db

from .user.user_role import UserRole
from .state.state import State
from .drug.drug_type import DrugType
from .blood_type.blood_type import BloodType

from .user.user import User
from .user.patient.patient import Patient

from .institution.pharmacy.pharmacy import Pharmacy
from .institution.hospital.hospital import Hospital

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
    _generate_patient()

    _generate_pharmacy()
    _generate_hospital()

    _generate_drugs()


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

    user = User.query.filter(User.username == UserRole.PATIENT.value).first()
    patient = Patient()
    patient.first_name = "Some"
    patient.last_name = "Patient"
    patient.address = "123 Patient St"
    patient.city = "Everytown"
    patient.state = State.NORTH_CAROLINA
    patient.zip = 12345
    patient.drug_type = DrugType.Generic
    patient.blood_type = BloodType.ONeg
    patient.user = user

    db.session.add(patient)

    db.session.commit()


def _generate_pharmacy():
    """
    Generates a pharmacy
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
    Generates a hospital
    """

    h = Hospital()
    h.name = "hospital"
    h.address = "123 Hospitla St"
    h.city = "Everytown"
    h.state = State.NORTH_CAROLINA
    h.zip = 12345

    db.session.add(h)
    db.session.commit()


def _generate_drugs():
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
