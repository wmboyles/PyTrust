"""
This file contains routes for the pages a labtech can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from ...decorators import has_roles

labtech_view_controller = Blueprint("labtech_view_controller",
                                    __name__,
                                    template_folder="templates",
                                    static_folder="static",
                                    url_prefix="/labtech")

BASE_FILE_URL = "labtech/"


@labtech_view_controller.route("/")
@has_roles(roles=["labtech"], return_if_fail=redirect("/login"))
def home():
    return render_template(BASE_FILE_URL + "index.html")
