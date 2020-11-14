"""
This file contains routes for the pages a personnel can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from ...decorators import has_roles

personnel_view_controller = Blueprint("personnel_view_controller",
                                      __name__,
                                      template_folder="templates",
                                      static_folder="static",
                                      url_prefix="/personnel")

BASE_FILE_URL = "personnel/"
RETURN_IF_FAIL = redirect("/login")


@personnel_view_controller.route("/demographics")
@has_roles(roles=['hcp', 'pharmacist'], return_if_fail=RETURN_IF_FAIL)
def edit_demographics():
    return render_template(BASE_FILE_URL + "editDemographics.html")
