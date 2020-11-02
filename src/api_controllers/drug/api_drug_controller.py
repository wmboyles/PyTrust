from flask import Blueprint, jsonify, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from ...persistent.persistent import db
from ...persistent.drug.drug import Drug, DrugSchema
from ...persistent.drug.drug_type import DrugType

# Controller blueprint that's exported to parent module to be registered
api_drug_controller = Blueprint("api_drug_controller",
                                __name__,
                                template_folder="templates",
                                static_folder="static",
                                url_prefix="/")


@api_drug_controller.route("/drugs", methods=['GET'])
def get_all_drugs():
    all_drugs = Drug.query.all()

    drug_schema = DrugSchema(many=True)
    out_drugs = drug_schema.dump(all_drugs)

    return jsonify(out_drugs), HTTPStatus.OK


@api_drug_controller.route("/drugs", methods=["POST"])
def make_drug():
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
def get_all_drug_types():
    drug_types = [dt.value for dt in DrugType]

    return jsonify(drug_types), HTTPStatus.OK