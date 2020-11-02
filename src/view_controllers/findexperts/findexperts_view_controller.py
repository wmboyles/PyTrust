from flask import Blueprint, render_template

findexperts_view_controller = Blueprint("findexperts_view_controller",
                                        __name__,
                                        template_folder="templates",
                                        static_folder="static",
                                        url_prefix="/findexperts")

BASE_FILE_URL = "findexperts/"


@findexperts_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")
