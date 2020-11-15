"""
This file contains API methods that relate to hospitals.
This includes CRUD operations on hospital objects.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from ....models.persistent.persistent import db
from ....models.persistent.institution.hospital.hospital import Hospital, HospitalSchema
from ....decorators import has_roles

api_hospital_controller = Blueprint(
    "api_hospital_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_hospital_controller.route("/hospitals", methods=["GET"])
@has_roles(roles=["admin", "patient", "hcp"])
def get_all_hospitals():
    """
    Gets a list of all hospitals in the DB
    """

    all_hospitals = Hospital.query.all()

    hospital_schema = HospitalSchema(many=True)
    out_hospitals = hospital_schema.dump(all_hospitals)

    return jsonify(out_hospitals), HTTPStatus.OK


@api_hospital_controller.route("/hospitals", methods=["POST"])
@has_roles(roles=["admin", "patient", "hcp"])
def make_hospital():
    """
    Creates a hospital
    """

    json_data = request.json

    if json_data.get("id") is not None:
        return "Cannot assign hospital id", HTTPStatus.BAD_REQUEST

    hospital_schema = HospitalSchema()
    try:
        hospital = hospital_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    try:
        db.session.add(hospital)
        db.session.commit()
    except IntegrityError as e:
        return "Already a hospital with that location", HTTPStatus.CONFLICT

    out_hospital = hospital_schema.dump(hospital)
    return out_hospital, HTTPStatus.OK


@api_hospital_controller.route("/hospitals", methods=["PUT"])
@has_roles(roles=["admin", "patient", "hcp"])
def edit_hospital():
    """
    Edits an existing hospital
    """

    json_data = request.json

    hospital_schema = HospitalSchema()
    try:
        new_hospital = hospital_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    old_hospital = Hospital.query.get(new_hospital.id)
    if old_hospital is None:
        return "No hospital with that id", HTTPStatus.NOT_FOUND

    db.session.merge(new_hospital)
    db.session.commit()

    out_hospital = hospital_schema.dump(new_hospital)
    return out_hospital, HTTPStatus.OK


@api_hospital_controller.route("/hospitals/<int:id>", methods=["DELETE"])
@has_roles(roles=["admin", "patient", "hcp"])
def delete_hospital(id):
    """
    Deletes a hospital with a given id

    :param id:: id of hospital in the db to delete
    """

    hospital = Hospital.query.get(id)

    if hospital is None:
        return "No hospital with that id", HTTPStatus.NOT_FOUND

    db.session.delete(hospital)
    db.session.commit()

    return "Successfully deleted hospital", HTTPStatus.OK