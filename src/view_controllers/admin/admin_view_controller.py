from flask import Blueprint, render_template, redirect

from ...decorators import has_roles

admin_view_controller = Blueprint("admin_view_controller",
                                  __name__,
                                  template_folder="templates",
                                  static_folder="static",
                                  url_prefix="/admin")

BASE_FILE_URL = "admin/"


@admin_view_controller.route("/")
# has_role must be inside route
@has_roles(roles=["admin"], return_if_fail=redirect("/login"))
def home():
    return render_template(BASE_FILE_URL + "index.html")