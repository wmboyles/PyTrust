"""
This file essentially list all the api blueprints and saves them in a
collection that can be imported by the main app. This is meant to cut down on
the number of imports in the main app and make it easier to add and remove
apis.

:author William Boyles:
"""

from .drug import api_drug_controller as drug
from .user import api_user_controller as user
from .user.patient import api_patient_controller as patient
from .user.personnel import api_personnel_controller as personnel
from .institution.pharmacy import api_pharmacy_controller as pharmacy
from .institution.hospital import api_hospital_controller as hospital
from .state import api_state_controller as state
from .blood_type import api_blood_type_controller as blood_type
from .ethnicity import api_ethnicity_controller as ethnicity

# All api prefixes begin with /api
BASE_URL = "/api"

# Collection of blueprints
blueprints = {
    drug.api_drug_controller,
    user.api_user_controller,
    patient.api_patient_controller,
    personnel.api_personnel_controller,
    pharmacy.api_pharmacy_controller,
    hospital.api_hospital_controller,
    state.api_state_controller,
    blood_type.api_blood_type_controller,
    ethnicity.api_ethnicity_controller,
}
