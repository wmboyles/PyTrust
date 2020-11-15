"""
This file contains the gender enum

:author William Boyles:
"""

import enum


class Gender(enum.Enum):
    """
    Gender is an enum that contains a patient's gender information
    """

    Male = "Male"
    Female = "Female"
    Other = "Other"
