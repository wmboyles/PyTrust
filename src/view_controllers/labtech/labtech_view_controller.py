from flask import Blueprint, render_template

labtech_view_controller = Blueprint("labtech_view_controller",
                                    __name__,
                                    template_folder="templates",
                                    static_folder="static",
                                    url_prefix="/labtech")

BASE_FILE_URL = "labtech/"


@labtech_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
