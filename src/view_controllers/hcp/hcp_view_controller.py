from flask import Blueprint, render_template

hcp_view_controller = Blueprint("hcp_view_controller",
                                __name__,
                                template_folder="templates",
                                static_folder="static",
                                url_prefix="/hcp")

BASE_FILE_URL = "hcp/"


@hcp_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
