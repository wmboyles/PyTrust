from flask import Blueprint, render_template

patient_view_controller = Blueprint("patient_view_controller",
                                    __name__,
                                    template_folder="templates",
                                    static_folder="static",
                                    url_prefix="/patient")

BASE_FILE_URL = "patient/"


@patient_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
