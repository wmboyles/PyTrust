"""
This file contains routes for the pages a patient can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from ...decorators import has_roles

patient_view_controller = Blueprint("patient_view_controller",
                                    __name__,
                                    template_folder="templates",
                                    static_folder="static",
                                    url_prefix="/patient")

BASE_FILE_URL = "patient/"


@patient_view_controller.route("/")
@has_roles(roles=["patient"], return_if_fail=redirect("/login"))
def home():
    return render_template(BASE_FILE_URL + "index.html")
