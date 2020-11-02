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

    PATIENT = "patient", "patient/index"
    HCP = "hcp", "hcp/index"
    ADMIN = "admin", "admin/index"
    ER = "er", "er/index"
    LABTECH = "labtech", "labtech/index"
    OD = "od", "hcp/index"
    OPH = "oph", "hcp/index"
    VIROLOGIST = "virologist", "hcp/index"
    PHARMACIST = "pharmacist", "pharmacist/index"
