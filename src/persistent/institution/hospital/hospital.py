"""
This file contians class information on hospitals, including the fields and
methods a hospital has in the hospital class, as well as how the hospital is
serialized as JSON in HospitalSchema.

:author William Boyles:
"""

from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from sqlalchemy.sql.schema import UniqueConstraint

from ...persistent import ma
from ..instutitution import Institution
from ...state.state import State


class Hospital(Institution):
    # Impose a unique constraint on name
    __table_args__ = (UniqueConstraint('name'), )


class HospitalSchema(ma.SQLAlchemyAutoSchema):
    """
    The hospital schema help with serialization and deserialization of hospitals
    """
    class Meta:
        include_fk = True
        model = Hospital

    @post_load
    def make_hospital(self, data: dict, **kwargs) -> Hospital:
        """
        This method is called when calling a load. It transforms a dictionary
        representing the object into the object itself.

        :param data: Dict data representing hospital object
        """

        return Hospital(**data)

    state = EnumField(State, by_value=True)