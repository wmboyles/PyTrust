from flask import Blueprint, render_template

personnel_view_controller = Blueprint("personnel_view_controller",
                                      __name__,
                                      template_folder="templates",
                                      static_folder="static",
                                      url_prefix="/personnel")

BASE_FILE_URL = "personnel/"


@personnel_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
