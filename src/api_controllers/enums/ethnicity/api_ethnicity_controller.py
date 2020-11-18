"""
This file contains API methods that relate to ethnicity.

:author William Boyles:
"""

from flask import Blueprint, jsonify
from http import HTTPStatus

from src.models.enums.ethnicity.ethnicity import Ethnicity

api_ethnicity_controller = Blueprint(
    "api_ethnicity_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_ethnicity_controller.route("/ethnicities", methods=["GET"])
def get_all_ethnicities():
    """
    Gets a list of all ethnicties defined in the ethnicity enum
    """

    ethnicities = [eth.value for eth in Ethnicity]

    return jsonify(ethnicities), HTTPStatus.OK
