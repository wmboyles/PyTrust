"""
This file contains routes for the pages a pharmacist can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from ....decorators import has_roles

pharmacist_view_controller = Blueprint("pharmacist_view_controller",
                                       __name__,
                                       template_folder="templates",
                                       static_folder="static",
                                       url_prefix="/pharmacist")

BASE_FILE_URL = "personnel/pharmacist/"


@pharmacist_view_controller.route("/")
@has_roles(roles=["pharmacist"], return_if_fail=redirect("/login"))
def home():
    return render_template(BASE_FILE_URL + "index.html")
