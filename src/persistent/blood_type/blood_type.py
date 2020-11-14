"""
This file contains the blood type enum

:author William Boyles:
"""

import enum


class BloodType(enum.Enum):
    """
    A blood type is a piece of health-related information that PyTrust stores about patients.
    """

    APos = "A+"
    ANeg = "A-"
    BPos = "B+"
    OPos = "O+"
    ONeg = "O-"
    ABPos = "AB+"
    ABNeg = "AB-"