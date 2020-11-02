"""
A drug type is an enum that describes the type of drug.
"""

import enum


class DrugType(enum.Enum):
    Generic = "Generic"
    Brand = "Brand"
    Not_Specified = "Not Specified"