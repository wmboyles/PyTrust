from flask import Blueprint, render_template

admin_view_controller = Blueprint("admin_view_controller",
                                  __name__,
                                  template_folder="templates",
                                  static_folder="static",
                                  url_prefix="/admin")

BASE_FILE_URL = "admin/"


@admin_view_controller.route("/")
def home():
    return render_template(BASE_FILE_URL + "index.html")