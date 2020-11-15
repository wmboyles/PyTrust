"""
This file contains API methods related to drugs.
This includes CRUD operations on Drug objects.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from ...models.persistent.persistent import db
from ...models.persistent.drug.drug import Drug, DrugSchema
from ...decorators import has_roles

# Controller blueprint that's exported to parent module to be registered
api_drug_controller = Blueprint(
    "api_drug_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_drug_controller.route("/drugs", methods=["GET"])
@has_roles(roles=["admin", "hcp", "pharmacist"])
def get_all_drugs():
    """
    Gets a list of all drugs in the database.
    """

    all_drugs = Drug.query.all()

    drug_schema = DrugSchema(many=True)
    out_drugs = drug_schema.dump(all_drugs)

    return jsonify(out_drugs), HTTPStatus.OK


@api_drug_controller.route("/drugs", methods=["POST"])
@has_roles(roles=["admin"])
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

    try:
        db.session.add(drug)
        db.session.commit()
    except IntegrityError as e:
        return "Combination of code and type must be unique", HTTPStatus.CONFLICT

    out_drug = drug_schema.dump(drug)
    # You only need to jsonify collections if you've used marshmallow shemas
    return out_drug, HTTPStatus.OK


@api_drug_controller.route("/drugs", methods=["PUT"])
@has_roles(roles=["admin"])
def edit_drug():
    """
    Edits an existing drug
    """

    json_data = request.json

    drug_schema = DrugSchema()
    try:
        new_drug = drug_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    old_drug = Drug.query.get(new_drug.id)
    if old_drug is None:
        return "No drug with that id", HTTPStatus.NOT_FOUND

    try:
        # merge existing and new, matched by id, keep new when differences
        db.session.merge(new_drug)
        db.session.commit()
    except IntegrityError as e:
        return "Combination of code and type must be unique", HTTPStatus.CONFLICT

    out_drug = drug_schema.dump(new_drug)
    return out_drug, HTTPStatus.OK


@api_drug_controller.route("/drugs/<int:id>", methods=["DELETE"])
@has_roles(roles=["admin"])
def delete_drug(id: int):
    """
    Deletes a drug with a given id

    :param id: id of Drug in the db to delete
    """

    drug = Drug.query.get(id)
    if drug is None:
        return "No drug with that id", HTTPStatus.NOT_FOUND

    db.session.delete(drug)
    db.session.commit()

    return "Successfully deleted drug", HTTPStatus.OK
