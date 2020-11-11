"""
This file contains API methods related to drugs.
This includes CRUD operations on Drug objects, as well as related items like
drug types.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from ...persistent.persistent import db
from ...persistent.drug.drug import Drug, DrugSchema
from ...persistent.drug.drug_type import DrugType
from ...decorators import has_roles

# Controller blueprint that's exported to parent module to be registered
api_drug_controller = Blueprint("api_drug_controller",
                                __name__,
                                template_folder="templates",
                                static_folder="static",
                                url_prefix="/")


@api_drug_controller.route("/drugs", methods=['GET'])
@has_roles(roles=['admin', 'hcp', 'pharmacist'])
def get_all_drugs():
    """
    Gets a list of all drugs in the database.
    """

    all_drugs = Drug.query.all()

    drug_schema = DrugSchema(many=True)
    out_drugs = drug_schema.dump(all_drugs)

    return jsonify(out_drugs), HTTPStatus.OK


@api_drug_controller.route("/drugs", methods=["POST"])
@has_roles(roles=['admin'])
def make_drug():
    """
    Creates a drug
    """

    json_data = request.json

    drug_schema = DrugSchema()
    try:
        drug = drug_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    db_drug = Drug.query.filter(Drug.name == drug.name).first()
    if db_drug:
        return "Drug with that name already exists", HTTPStatus.CONFLICT

    db.session.add(drug)
    db.session.commit()

    out_drug = drug_schema.dump(drug)
    # You only need to jsonify collections if you've used marshmallow shemas
    return out_drug, HTTPStatus.OK


@api_drug_controller.route("/drug_types", methods=["GET"])
@has_roles(roles=['admin', 'patient'])
def get_all_drug_types():
    """
    Gets a list of all drugtypes defined by the DrugType enum.
    """

    drug_types = [dt.value for dt in DrugType]

    return jsonify(drug_types), HTTPStatus.OK