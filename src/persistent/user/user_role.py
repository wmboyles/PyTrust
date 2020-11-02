"""
A user role is an enum that describes what sort of user is logged in.
Several views and API calls may be restricted to certain user roles.
"""

import enum


class UserRole(enum.Enum):
    # Have to override this to serialize correctly
    def __new__(cls, *args, **kwds):
        value = args[0]  # Gets by first attribe: role name
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, role_name, landing_page):
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
