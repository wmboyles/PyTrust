"""
This file contains the drug type enum.

:author William Boyles:
"""

import enum


class DrugType(enum.Enum):
    """
    A drug type is an enum that describes the type of drug.
    """

    Generic = "Generic"
    Brand = "Brand"
    Not_Specified = "Not Specified"