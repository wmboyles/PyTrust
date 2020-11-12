"""
This file contains routes for the pages an admin can see.

:author William Boyles:
"""

from flask import Blueprint, render_template, redirect

from ...decorators import has_roles

admin_view_controller = Blueprint("admin_view_controller",
                                  __name__,
                                  template_folder="templates",
                                  static_folder="static",
                                  url_prefix="/admin")

BASE_FILE_URL = "admin/"
RETURN_IF_FAIL = redirect("/login")


@admin_view_controller.route("/")
@has_roles(roles=["admin"], return_if_fail=RETURN_IF_FAIL)
def home():
    return render_template(BASE_FILE_URL + "index.html")


@admin_view_controller.route("/drugs")
@has_roles(roles=['admin'], return_if_fail=RETURN_IF_FAIL)
def manage_drugs():
    return render_template(BASE_FILE_URL + "drugs.html")