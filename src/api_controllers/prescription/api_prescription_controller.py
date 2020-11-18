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

    # we have to do a tiny bit of merging manually
    prescription.prescriber.user_id = prescription.prescriber.user.id
    prescription.patient.user_id = prescription.patient.user.id

    db.session.merge(prescription)
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

    # we have to do a tiny bit of merging manually
    new_prescription.prescriber.user_id = new_prescription.prescriber.user.id
    new_prescription.patient.user_id = new_prescription.patient.user.id

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

    return "Successfully deleted prescription", HTTPStatus.OK


@api_prescription_controller.route("/prescriptions/fill/<int:id>", methods=["PUT"])
@has_roles(roles=["pharmacist"])
def fill_prescription(id: int):
    """
    Fills a prescription with a given id. This decreases the number of renewals by 1.
    If the prescription has used all its renewals so that it could ont be filled again, it will be deleted.

    :param id: id of Prescription to fill
    """

    target_prescription = Prescription.query.get(id)
    if target_prescription is None:
        return "No prescription with that id", HTTPStatus.NOT_FOUND

    calling_user = User.query.filter(User.username == session.get("username")).one()
    calling_pharmacist = Personnel.query.get(calling_user.id)
    if calling_pharmacist is None:
        return "No personnel with calling username", HTTPStatus.NOT_FOUND

    if target_prescription.pharmacy != calling_pharmacist.pharmacy:
        return (
            "Calling pharmacist does not work at prescription's pharmacy",
            HTTPStatus.UNAUTHORIZED,
        )

    if target_prescription.renewals == 0:
        db.session.delete(target_prescription)
    else:
        target_prescription.renewals -= 1

    db.session.commit()

    return "Successfully filled prescription", HTTPStatus.OK
