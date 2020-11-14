"""
This file contains the ethnicity enum

:author William Boyles:
"""

import enum


class Ethnicity(enum.Enum):
    """
    Ethnicity is a enum that contains a patient's ethnic information
    """

    White = "White"
    Black = "Black"
    Hispanic = "Hispanic"
    Native = "Native/Aborigonal"
    Asian = "Asian"
    Other = "Other"
