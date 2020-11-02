from flask import Blueprint, render_template

login_view_controller = Blueprint("login_view_controller",
                                  __name__,
                                  template_folder="templates",
                                  static_folder="static",
                                  url_prefix="/")

BASE_FILE_URL = "login/"


@login_view_controller.route("/", methods=['GET'])
@login_view_controller.route("/login", methods=['GET'])
def login_home():
    return render_template(BASE_FILE_URL + "login.html")