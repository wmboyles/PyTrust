"""
This file generates sample data in the database

:author William Boyles:
"""

from .persistent import db

from .user.user_role import UserRole
from .state.state import State
from .user.user import User
from .user.patient.patient import Patient

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
    patient.address = "1234 Street Rd."
    patient.city = "Everytown"
    patient.state = State.NORTH_CAROLINA
    patient.zip = 12345
    patient.user = user

    db.session.add(patient)

    db.session.commit()
