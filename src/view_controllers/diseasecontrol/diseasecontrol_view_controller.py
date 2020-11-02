from flask import Blueprint, render_template

diseasecontrol_view_controller = Blueprint("diseasecontrol_view_controller",
                                           __name__,
                                           template_folder="templates",
                                           static_folder="static",
                                           url_prefix="/diseasecontrol")

BASE_FILE_URL = "diseasecontrol/"


@diseasecontrol_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
