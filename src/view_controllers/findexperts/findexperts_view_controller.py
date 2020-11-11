"""
This file contains routes for the pages related to finding an expert

:author William Boyles:
"""

from flask import Blueprint, render_template

from ...decorators import has_roles

findexperts_view_controller = Blueprint("findexperts_view_controller",
                                        __name__,
                                        template_folder="templates",
                                        static_folder="static",
                                        url_prefix="/findexperts")

BASE_FILE_URL = "findexperts/"


# TODO: Does this need any controllers?
@findexperts_view_controller.route("/")
@has_roles(roles=['hcp', 'patient'])
def home():
    return render_template(BASE_FILE_URL + "index.html")
