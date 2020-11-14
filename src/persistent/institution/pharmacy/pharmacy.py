"""
This file contians class information on pharmacies, including the fields and
methods a pharmacy has in the Pharmacy class, as well as how the pharmacy is
serialized as JSON in PharmacySchema.

:author William Boyles:
"""

from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from sqlalchemy.sql.schema import UniqueConstraint

from ...persistent import ma
from ..instutitution import Institution
from ...state.state import State


class Pharmacy(Institution):
    # Impose a unique constraint on combination of location fields
    __table_args__ = (UniqueConstraint("address", "city", "state", "zip"),)


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
        This method is called when calling a load. It transforms a dictionary
        representing the object into the object itself.

        :param data: Dict data representing pharmacy object
        """

        return Pharmacy(**data)

    state = EnumField(State, by_value=True)