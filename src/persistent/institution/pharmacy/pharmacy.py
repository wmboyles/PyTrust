"""
This file contians class information on pharmacies, including the fields and
methods a pharmacy has in the Pharmacy class, as well as how the pharmacy is
serialized as JSON in PharmacySchema
"""

from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from sqlalchemy.orm import validates
from sqlalchemy.sql.schema import UniqueConstraint

from ...persistent import db, ma
from ...state.state import State


class Pharmacy(db.Model):
    """
    A pharmacy is a location where patients can get their prescriptions filled.

    :param id: Unique if in the database
    :param name: name of pharmacy. Does not have to be unique
    :param address: Street address of pharmacy
    :param city: City where pharmacy is located
    :param state: State where pharmacy is located
    :param zip: Zip code where pharmacy is located
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    address = db.Column(db.String(127), nullable=False)
    city = db.Column(db.String(127), nullable=False)
    state = db.Column(db.Enum(State), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

    # Impose a unique constraint on combination of location fields
    __table_args__ = (UniqueConstraint('address', 'city', 'state', 'zip'), )

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


class PharmacySchema(ma.SQLAlchemyAutoSchema):
    """
    The pharmacy schema help with serialization and deserialization of pharmacies
    """
    class Meta:
        include_fk = True
        model = Pharmacy

    @post_load
    def make_pharmacy(self, data: dict, **kwargs) -> Pharmacy:
        """
        This method is called when calling a lod. It transforms a dictionary
        representing the object into the object itself.

        :param data: Dict data representing pharmacy object
        """

        return Pharmacy(**data)

    state = EnumField(State, by_value=True)