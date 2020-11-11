from flask import Blueprint, render_template, redirect

from ...decorators import has_roles

BASE_URL = "/er"

er_view_controller = Blueprint("er_view_controller",
                               __name__,
                               template_folder="templates",
                               static_folder="static",
                               url_prefix="/er")

BASE_FILE_URL = "er/"


@er_view_controller.route("/")
@has_roles(roles=["er"], return_if_fail=redirect("/login"))
def home():
    return render_template(BASE_FILE_URL + "index.html")
