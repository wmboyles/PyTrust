"""
This file imports and contains a collection of all api controllers.
This file exists to cut down on the number of imports in the app.py file.

:author William Boyles:
"""

from .login import login_view_controller as login

from .admin import admin_view_controller as admin
from .patient import patient_view_controller as patient

# from .diseasecontrol import diseasecontrol_view_controller as diseasecontrol
# from .er import er_view_controller as er
# from .findexperts import findexperts_view_controller as findexperts
# from .labtech import labtech_view_controller as labtech

from .personnel import personnel_view_controller as personnel
from .personnel.hcp import hcp_view_controller as hcp
from .personnel.pharmacist import pharmacist_view_controller as pharmacist

# Base URL is defined by each blueprint, but keeps consistency with API
BASE_URL = None

# Collection of view controller blueprints
view_controllers = {
    login.login_view_controller,
    admin.admin_view_controller,
    patient.patient_view_controller,
    # diseasecontrol.diseasecontrol_view_controller,
    # er.er_view_controller,
    # findexperts.findexperts_view_controller,
    # labtech.labtech_view_controller,
    personnel.personnel_view_controller,
    hcp.hcp_view_controller,
    pharmacist.pharmacist_view_controller,
}
