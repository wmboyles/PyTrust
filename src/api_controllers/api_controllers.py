"""
This file imports and contains a collection of all api controllers.
It specifies a url prefix for all api controllers so the routes don't conflict with view controllers.
This file exists to cut down on the number of imports in the app.py file.

:author William Boyles:
"""

from .drug import api_drug_controller as drug
from .user import api_user_controller as user
from .user.patient import api_patient_controller as patient
from .user.personnel import api_personnel_controller as personnel
from .institution.pharmacy import api_pharmacy_controller as pharmacy
from .institution.hospital import api_hospital_controller as hospital
from .prescription import api_prescription_controller as prescription
from .enums.api_enum_controllers import api_enum_controllers


# All api prefixes begin with /api
BASE_URL = "/api"

# Collection of api_controller blueprints
api_controllers = {
    drug.api_drug_controller,
    user.api_user_controller,
    patient.api_patient_controller,
    personnel.api_personnel_controller,
    pharmacy.api_pharmacy_controller,
    hospital.api_hospital_controller,
    prescription.api_prescription_controller,
    *api_enum_controllers,
}
