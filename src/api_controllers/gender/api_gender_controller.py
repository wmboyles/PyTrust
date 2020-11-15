"""
This file contians API methods that relate to gender

:author William Boyles:
"""

from flask import Blueprint, jsonify
from http import HTTPStatus

from ...models.persistent.gender.gender import Gender

api_gender_controller = Blueprint(
    "api_gender_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_gender_controller.route("/genders", methods=["GET"])
def get_all_genders():
    """
    Gets a list of all genders defined in the gender enum
    """

    genders = [gen.value for gen in Gender]

    return jsonify(genders), HTTPStatus.OK
