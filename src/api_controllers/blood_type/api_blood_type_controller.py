"""
This file contains API methods that relate to blood types.

:author William Boyles:
"""

from flask import Blueprint, jsonify
from http import HTTPStatus

from ...models.persistent.blood_type.blood_type import BloodType

api_blood_type_controller = Blueprint(
    "api_blood_type_controlller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_blood_type_controller.route("/blood_types", methods=["GET"])
def get_all_blood_types():
    """
    Gets a list of all blood types defined in the blood type enum
    """

    blood_types = [bt.value for bt in BloodType]

    return jsonify(blood_types), HTTPStatus.OK
