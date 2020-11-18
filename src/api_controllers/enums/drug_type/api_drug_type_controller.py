"""
This file contains API methods that relate to drug types

:author William Boyles
"""

from flask import Blueprint, jsonify
from http import HTTPStatus

from src.models.enums.drug_type.drug_type import DrugType
from src.decorators import has_roles

api_drug_type_controller = Blueprint(
    "api_drug_type_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_drug_type_controller.route("/drug_types")
@has_roles(roles=["admin", "patient", "hcp"])
def get_all_drug_types():
    """
    Gets a list of all drugtypes defined by the DrugType enum.
    """

    drug_types = [dt.value for dt in DrugType]

    return jsonify(drug_types), HTTPStatus.OK
