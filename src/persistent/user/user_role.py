"""
This file contains the UserRole enum

:author William Boyles:
"""

import enum


class UserRole(enum.Enum):
    """
    A user role is an enum that describes what sort of user is logged in.
    Several views and API calls may be restricted to certain user roles.
    """
    def __new__(cls, *args, **kwargs):
        """
        Provides non-default way to construct UserRole.
        """
        value = args[0]  # Gets by first attribute: role name
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, role_name, landing_page):
        """
        Creates a new UserRole object.

        :param role_name: name of the role
        :param landing_page: main landing page when user with given role logs in
        """

        self.role_name = role_name
        self.landing_page = landing_page

    PATIENT = "patient", "patient"
    HCP = "hcp", "hcp"
    ADMIN = "admin", "admin"
    ER = "er", "er"
    LABTECH = "labtech", "labtech"
    OD = "od", "hcp"
    OPH = "oph", "hcp"
    VIROLOGIST = "virologist", "hcp"
    PHARMACIST = "pharmacist", "pharmacist"
