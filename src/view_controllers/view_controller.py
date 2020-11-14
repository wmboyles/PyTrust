"""
This file essentially imports a list of all view blueprints and saves them in a
collection that can be imported by the main app. This is meant to cut down on
the number of imports in the main app and make it easier to add and remove
views.

:author William Boyles:
"""

from .login import login_view_controller as login
from .admin import admin_view_controller as admin
#from .diseasecontrol import diseasecontrol_view_controller as diseasecontrol
#from .er import er_view_controller as er
#from .findexperts import findexperts_view_controller as findexperts
from .personnel.hcp import hcp_view_controller as hcp
#from .labtech import labtech_view_controller as labtech
from .patient import patient_view_controller as patient
from .personnel import personnel_view_controller as personnel
from .personnel.pharmacist import pharmacist_view_controller as pharmacist

# Base URL is defined by each blueprint, but keeps consistency with API
BASE_URL = None

# Collection of blueprints
blueprints = {
    login.login_view_controller,
    admin.admin_view_controller,
    #diseasecontrol.diseasecontrol_view_controller,
    #er.er_view_controller,
    #findexperts.findexperts_view_controller,
    hcp.hcp_view_controller,
    #labtech.labtech_view_controller,
    patient.patient_view_controller,
    personnel.personnel_view_controller,
    pharmacist.pharmacist_view_controller,
}
