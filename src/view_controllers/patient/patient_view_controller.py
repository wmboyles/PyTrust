"""
This file contains routes for the pages a patient can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from src.decorators import has_roles

patient_view_controller = Blueprint(
    "patient_view_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/patient",
)

BASE_FILE_URL = "patient/"
RETURN_IF_FAIL = redirect("/login")


@patient_view_controller.route("/")
@has_roles(roles=["patient"], return_if_fail=RETURN_IF_FAIL)
def home():
    return render_template(BASE_FILE_URL + "index.html")


@patient_view_controller.route("/demographics")
@has_roles(roles=["patient"], return_if_fail=RETURN_IF_FAIL)
def edit_demographics():
    return render_template(BASE_FILE_URL + "editDemographics.html")


@patient_view_controller.route("/prescriptions")
@has_roles(roles=["patient"], return_if_fail=RETURN_IF_FAIL)
def view_prescriptions():
    return render_template(BASE_FILE_URL + "viewPrescriptions.html")
