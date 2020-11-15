"""
This file contains API methods that relate to user roles

:author William Boyles:
"""

from flask import Blueprint, jsonify
from http import HTTPStatus

from ....models.enums.user_role.user_role import UserRole
from ....decorators import has_roles

api_user_role_controller = Blueprint(
    "api_user_role_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_user_role_controller.route("/user_roles")
@has_roles(roles=["admin"])
def get_all_user_roles():
    """
    Gets a list of all user roles defined in the UserRole enum.
    """

    user_roles = [role.value for role in UserRole]

    return jsonify(user_roles), HTTPStatus.OK
