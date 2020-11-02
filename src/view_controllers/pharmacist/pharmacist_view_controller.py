from flask import Blueprint, render_template

pharmacist_view_controller = Blueprint("pharmacist_view_controller",
                                       __name__,
                                       template_folder="templates",
                                       static_folder="static",
                                       url_prefix="/pharmacist")

BASE_FILE_URL = "pharmacist/"


@pharmacist_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
