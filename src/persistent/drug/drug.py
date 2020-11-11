"""
This file contains stores class infomation on drugs, including the fields and
methods a drug has in the Drug class, as well as how the drug is serialized as
JSON in DrugSchema.

:author William Boyles:
"""

from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from sqlalchemy.orm import validates
import re

from ..persistent import db, ma
from .drug_type import DrugType


class Drug(db.Model):
    """
    A Drug is a medicine that HCPs can prescribe to patients.

    :param id: Unique id in the database. Is set automatically.
    :param name: Unique chemical name.
    :param code: NDC code. Must be formatted "####-####-##"
    :param description: Longer description of the drug's properties
    :param type: Type. Either Generic or Branded
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False, unique=True)
    code = db.Column(db.String(12), nullable=False)
    description = db.Column(db.String(1023), nullable=False)
    type = db.Column(db.Enum(DrugType), nullable=False)

    # You only need @validates methods on fields where your column definitions
    # are not sufficient. You don't need to check for None or type in these
    # methods because that's handled by the oclumn definitions.

    @validates('code')
    def validate_code(self, key, code: str) -> str:
        """
        Validates that code field matches the required pattern.

        :param code: string NDC code to validate
        :return: validated NDC code
        :raises AssertionError: if code does not match pattern
        """

        if not re.fullmatch("\d{4}-\d{4}-\d{2}", code):
            raise AssertionError("Code does not match pattern")

        return code

    @validates('type')
    def validate_type(self, key, dtype: DrugType) -> DrugType:
        """
        Validates that the drug type field is not unspecified.

        :param dtype: DrugType to validate
        :returns: validated DrugType
        :raises AssertionError: if dtype is invalid
        """

        if dtype == DrugType.Not_Specified:
            raise AssertionError(
                "Drug type cannot be not specified for creating drugs")

        return dtype

    # Init method is taken care of by db.Model
    # You can add @classmethod annotations to build drug from other objects


class DrugSchema(ma.SQLAlchemyAutoSchema):
    """
    The drug shema helps with serialization and deserialization of drugs.
    """
    class Meta:
        include_fk = True
        model = Drug

    @post_load
    def make_drug(self, data: dict, **kwargs) -> Drug:
        """
        This method is called when calling a load. It transforms a dictionary
        representing the object into the object itself.

        :param data: Dict data representing drug object
        """

        return Drug(**data)

    # Enums have to be done a bit more explicitly to serialize correctly
    type = EnumField(DrugType, by_value=True)

    # include list of fields where you want to object rather than the key
    # things = ma.Nested("ThingSchema")