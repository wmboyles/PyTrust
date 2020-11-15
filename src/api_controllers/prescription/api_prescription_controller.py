"""
This file contains API methods related to prescriptions.
This includes CRUD operations on Prescription objects.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request, session
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from ...models.persistent.persistent import db
from ...models.persistent.prescription.prescription import (
    Prescription,
    PrescriptionSchema,
)
from ...models.persistent.user.user import User, UserRole
from ...models.persistent.user.personnel.personnel import Personnel
from ...models.persistent.user.patient.patient import Patient
from ...decorators import has_roles

api_prescription_controller = Blueprint(
    "api_prescription_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_prescription_controller.route("/prescriptions", methods=["GET"])
@has_roles(roles=["hcp", "pharmacist", "patient"])
def get_self_prescriptions():
    """
    Gets a list of all prescriptions related to the calling user
    """

    calling_username = session.get("username")
    calling_user = User.query.filter(User.username == calling_username).one()

    if calling_user.role == UserRole.HCP:
        target_caller = Personnel.query.get(calling_user.id)
    elif calling_user.role == UserRole.PHARMACIST:
        target_caller = Personnel.query.get(calling_user.id).pharmacy
    elif calling_user.role == UserRole.PATIENT:
        target_caller = Patient.query.get(calling_user.id)
    else:
        return "User doesn't have a valid role", HTTPStatus.UNAUTHORIZED

    prescription_schema = PrescriptionSchema(many=True)
    prescriptions = prescription_schema.dump(target_caller.prescriptions)

    return jsonify(prescriptions), HTTPStatus.OK


@api_prescription_controller.route("/prescriptions", methods=["POST"])
@has_roles(roles=["hcp"])
def make_prescription():
    """
    Creates a prescription
    """

    json_data = request.json

    prescription_schema = PrescriptionSchema()
    try:
        prescription = prescription_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    db.session.add(prescription)
    db.session.commit()

    out_prescription = prescription_schema.dump(prescription)
    return out_prescription, HTTPStatus.OK


@api_prescription_controller.route("/prescriptions", methods=["PUT"])
@has_roles(roles=["hcp"])
def edit_prescription():
    """
    Edits an exsiting prescription
    """

    json_data = request.json

    prescription_schema = PrescriptionSchema()
    try:
        new_prescription = prescription_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    old_prescription = Prescription.query.get(new_prescription.id)
    if old_prescription is None:
        return "No prescription with that id", HTTPStatus.NOT_FOUND

    db.session.merge(new_prescription)
    db.session.commit()

    out_prescription = prescription_schema.dump(new_prescription)
    return out_prescription, HTTPStatus.OK


@api_prescription_controller.route("/prescriptions/<int:id>", methods=["DELETE"])
@has_roles(roles=["hcp", "pharmacist"])
def delete_prescription(id: int):
    """
    Deletes a prescription with a given id

    :param id: id of Prescription in the db to delete
    """

    prescription = Prescription.query.get(id)
    if prescription is None:
        return "No prescription with that id", HTTPStatus.NOT_FOUND

    db.session.delete(prescription)
    db.session.commit()
