from flask import Blueprint, render_template

from ...decorators import has_roles

personnel_view_controller = Blueprint("personnel_view_controller",
                                      __name__,
                                      template_folder="templates",
                                      static_folder="static",
                                      url_prefix="/personnel")

BASE_FILE_URL = "personnel/"


# TODO: Does this blueprint need roles?
@personnel_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
