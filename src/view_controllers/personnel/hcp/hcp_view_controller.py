"""
This file contains routes for the pages a hcp can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from ....decorators import has_roles

hcp_view_controller = Blueprint(
    "hcp_view_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/hcp",
)

BASE_FILE_URL = "personnel/hcp/"
RETURN_IF_FAIL = redirect("/login")


@hcp_view_controller.route("/")
@has_roles(roles=["hcp"], return_if_fail=RETURN_IF_FAIL)
def home():
    return render_template(BASE_FILE_URL + "index.html")


@hcp_view_controller.route("/editpatientdemographics")
@has_roles(roles=["hcp"], return_if_fail=RETURN_IF_FAIL)
def edit_patient_demographics():
    return render_template(BASE_FILE_URL + "editPatientDemographics.html")
