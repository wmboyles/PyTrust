"""
This file contains the Personnel db model and marshmallow schema

:author William Boyles:
"""

from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from sqlalchemy.orm import validates

from ..user import User, UserRole
from ...institution.hospital.hospital import Hospital
from ...institution.pharmacy.pharmacy import Pharmacy
from ...persistent import db, ma
from ....enums.state.state import State


class Personnel(db.Model):
    """
    A personnel is a user who works in the capacity of an employee.
    They are differenciated from patients in that PyTrust stores less
    information about them, and they do not have the ability to have an office
    visit, receiveprescriptions, etc.
    """

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    # if user is deleted by admin, so is the personnel
    user = db.relationship(
        User, backref=db.backref("personnel", cascade="all, delete-orphan")
    )

    first_name = db.Column(db.String(127), nullable=False)
    last_name = db.Column(db.String(127), nullable=False)

    address = db.Column(db.String(127), nullable=False)
    city = db.Column(db.String(127), nullable=False)
    state = db.Column(db.Enum(State), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), nullable=True)
    hospital = db.relationship(Hospital, backref="employees")

    pharmacy_id = db.Column(db.Integer, db.ForeignKey("pharmacy.id"), nullable=True)
    pharmacy = db.relationship(Pharmacy, backref="employees")

    @validates("user")
    def validate_role(self, key, user: User) -> User:
        """
        Validates that the associated user's role is not a patient or admin.

        :param user: A user associated with this personnel
        :return: validated user
        :raises AssertionError: if user's role is a patient or admin
        """

        if user.role is UserRole.PATIENT:
            raise AssertionError("Must not be a patient")
        if user.role is UserRole.ADMIN:
            raise AssertionError("Must not be an admin")

        return user

    @validates("zip")
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


class PersonnelSchema(ma.SQLAlchemyAutoSchema):
    """
    The personnel schema help with the serialization and deserialization of personnel.
    """

    class Meta:
        model = Personnel

    @post_load
    def make_personnel(self, data: dict, **kwargs) -> Personnel:
        return Personnel(**data)

    user = ma.Nested("UserSchema")
    hospital = ma.Nested("HospitalSchema", allow_none=True)
    pharmacy = ma.Nested("PharmacySchema", allow_none=True)

    state = EnumField(State, by_value=True)