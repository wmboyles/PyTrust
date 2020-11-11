"""
This file contains routes for the pages a disease control user can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from ...decorators import has_roles

diseasecontrol_view_controller = Blueprint("diseasecontrol_view_controller",
                                           __name__,
                                           template_folder="templates",
                                           static_folder="static",
                                           url_prefix="/diseasecontrol")

BASE_FILE_URL = "diseasecontrol/"


@diseasecontrol_view_controller.route("/")
@has_roles(roles=["virologist"], return_if_fail=redirect("/login"))
def home():
    return render_template(BASE_FILE_URL + "index.html")
