"""
This file contains API methods that relate to pharmacies.
This includes CRUD operations on pharmacy objects.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from ...persistent.persistent import db
from ...persistent.institution.pharmacy.pharmacy import Pharmacy, PharmacySchema
from ...decorators import has_roles

api_pharmacy_controller = Blueprint("api_pharmacy_controller",
                                    __name__,
                                    template_folder="templates",
                                    static_folder="static",
                                    url_prefix="/")


@api_pharmacy_controller.route("/pharmacies", methods=['GET'])
@has_roles(roles=['admin', 'patient', 'hcp', 'pharmacist'])
def get_all_pharmacies():
    """
    Gets a list of all pharmacies in the DB
    """

    all_pharmacies = Pharmacy.query.all()

    pharmacy_schema = PharmacySchema(many=True)
    out_pharmacies = pharmacy_schema.dump(all_pharmacies)

    return jsonify(out_pharmacies), HTTPStatus.OK


@api_pharmacy_controller.route("/pharmacies", methods=['POST'])
@has_roles(roles=['admin', 'patient', 'hcp', 'pharmacist'])
def make_pharmacy():
    """
    Creates a pharmacy
    """

    json_data = request.json

    if json_data.get('id') is not None:
        return "Cannot assign pharmacy id", HTTPStatus.BAD_REQUEST

    pharmacy_schema = PharmacySchema()
    try:
        pharmacy = pharmacy_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    try:
        db.session.add(pharmacy)
        db.session.commit()
    except IntegrityError as e:
        return "Already a pharmacy with that location", HTTPStatus.CONFLICT

    out_pharmacy = pharmacy_schema.dump(pharmacy)
    return out_pharmacy, HTTPStatus.OK


@api_pharmacy_controller.route("/pharmacies", methods=['PUT'])
@has_roles(roles=['admin', 'patient', 'hcp', 'pharmacist'])
def edit_pharmacy():
    """
    Edits an existing pharmacy
    """

    json_data = request.json

    pharmacy_schema = PharmacySchema()
    try:
        new_pharmacy = pharmacy_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    old_pharmacy = Pharmacy.query.get(new_pharmacy.id)
    if old_pharmacy is None:
        return "No pharmacy with that id", HTTPStatus.NOT_FOUND

    db.session.merge(new_pharmacy)
    db.session.commit()

    out_pharmacy = pharmacy_schema.dump(new_pharmacy)
    return out_pharmacy, HTTPStatus.OK


@api_pharmacy_controller.route("/pharmacies/<int:id>", methods=['DELETE'])
@has_roles(roles=['admin', 'patient', 'hcp', 'pharmacist'])
def delete_pharmacy(id):
    """
    Deletes a pharmacy with a given id

    :param id:: id of Pharmacy in the db to delete
    """

    pharmacy = Pharmacy.query.get(id)

    if pharmacy is None:
        return "No pharmacy with that id", HTTPStatus.NOT_FOUND

    db.session.delete(pharmacy)
    db.session.commit()

    return "Successfully deleted pharmacy", HTTPStatus.OK