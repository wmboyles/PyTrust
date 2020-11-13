from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from sqlalchemy.orm import validates

from ..persistent import db, ma
from ..state.state import State


class Institution(db.Model):
    """
    A institution is a location where patients can get some of their healthcare needs met

    :param id: Unique if in the database
    :param name: name of pharmacy. Does not have to be unique
    :param address: Street address of pharmacy
    :param city: City where pharmacy is located
    :param state: State where pharmacy is located
    :param zip: Zip code where pharmacy is located
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    address = db.Column(db.String(127), nullable=False)
    city = db.Column(db.String(127), nullable=False)
    state = db.Column(db.Enum(State), nullable=False)
    zip = db.Column(db.Integer, nullable=False)

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