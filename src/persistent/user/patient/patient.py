"""
This file contains the Patient db model and marshmallow schema

:author William Boyles:
"""

from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from sqlalchemy.orm import validates

from ..user import User, UserRole
from ...persistent import db, ma
from ....persistent.state.state import State


class Patient(db.Model):
    """
    A Patient contains more specific demographics information about users with the patient role.

    :param user_id: Unique database id. This is the same id as the associated user, because all user ids are 
    :param user: The associated user. This will be generally how the userid field is set, by specifying the entire user object
    :param first_name: patient's first name
    :param last_name: patient's last name
    :param address: patient's street address
    :param city: patient's city
    :param state: patient's state of residence
    :param zip: patient's zip code
    """

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        primary_key=True,
                        unique=True,
                        nullable=False)
    # if user is deleted by admin, so is the patient
    user = db.relationship(User,
                           backref=db.backref('patient',
                                              cascade="all, delete-orphan"))

    first_name = db.Column(db.String(127), nullable=False)
    last_name = db.Column(db.String(127), nullable=False)

    address = db.Column(db.String(127), nullable=False)
    city = db.Column(db.String(127), nullable=False)
    state = db.Column(db.Enum(State), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

    @validates('user')
    def validate_role(self, key, user: User) -> User:
        """
        Validates that the associated user's role is a patient.

        :param user: A user associated with this patient
        :return: validated user
        :raises AssertionError: if user's role is not a patient
        """

        if user.role is not UserRole.PATIENT:
            raise AssertionError("Must be a patient")

        return user

    @validates('zip')
    def validate_zip(self, key, zip: int) -> int:
        """
        Validates that zip code field matches required pattern of five digits.

        :param zip: integer zip code:
        :return: validated zip code
        :raises AssertionError: if zip code is not five digits
        """

        if len(str(zip)) != 5:
            raise AssertionError("Zip code is not 5 digits")

        return zip


class PatientSchema(ma.SQLAlchemyAutoSchema):
    """
    The patient schema helps with the serialization and deserializaton of patients.
    """
    class Meta:
        model = Patient

    @post_load
    def make_patient(self, data: dict, **kwargs) -> Patient:
        return Patient(**data)

    # include list of fields where you want to object rather than the key
    user = ma.Nested("UserSchema")
    state = EnumField(State, by_value=True)
