"""
This file contains API methods that relate to patients.
This includes CRUD operations on patient objects.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request, session
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from ....persistent.persistent import db
from ....persistent.user.patient.patient import Patient, PatientSchema
from ....persistent.user.user import User, UserSchema
from ....decorators import has_roles

api_patient_controller = Blueprint("api_patient_controller",
                                   __name__,
                                   template_folder="templates",
                                   static_folder="static",
                                   url_prefix="/")


@api_patient_controller.route("/patients", methods=['GET'])
@has_roles(roles=['hcp'])
def get_all_patients():
    """
    Gets a list of all patients in the DB
    """

    all_patients = Patient.query.all()

    patient_schema = PatientSchema(many=True)
    out_patients = patient_schema.dump(all_patients)

    return jsonify(out_patients), HTTPStatus.OK


@api_patient_controller.route("/patients/self", methods=['GET'])
@has_roles(roles=['patient'])
def get_self_patient():
    """
    If there is an existing patient object corresponding to the calling user, return it
    """

    caller_username = session.get('username', None)
    if caller_username is None:
        return "No username in client session", HTTPStatus.NOT_FOUND

    calling_user = User.query.filter(User.username == caller_username).first()
    calling_patient = Patient.query.filter(
        Patient.user == calling_user).first()
    if calling_patient is None:
        user_schema = UserSchema()
        out_user = user_schema.dump(calling_user)

        # return user instead of patient
        return out_user, HTTPStatus.NOT_FOUND

    patient_schema = PatientSchema()
    out_patient = patient_schema.dump(calling_patient)

    return out_patient, HTTPStatus.OK


@api_patient_controller.route("/patients", methods=['POST'])
@has_roles(roles=['patient'])
def make_patient():
    """
    Creates a patient
    """

    json_data = request.json

    patient_schema = PatientSchema()
    try:
        patient = patient_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    user_id = patient.user.id
    db_user = User.query.get(user_id)
    if db_user is None:
        return "Provided user does not match existing user", HTTPStatus.NOT_FOUND

    # just comparing the user objects doesn't work. Have to look at serialization
    user_schema = UserSchema()
    db_user_json = user_schema.dump(db_user)
    patient_user_json = user_schema.dump(patient.user)
    if db_user_json != patient_user_json:
        return "Provided user's fields do not match stored fields", HTTPStatus.CONFLICT

    db_patient = Patient.query.get(user_id)
    if db_patient is not None:
        return "Already a patient for this user", HTTPStatus.CONFLICT

    # have to merge instead of commit b/c user field already exists
    db.session.merge(patient)
    db.session.commit()

    out_patient = patient_schema.dump(patient)
    return out_patient, HTTPStatus.OK


@api_patient_controller.route("/patients", methods=['PUT'])
@has_roles(roles=['hcp', 'patient'])
def edit_patient():
    """
    Edits an existing patient
    """

    json_data = request.json

    patient_schema = PatientSchema()
    try:
        new_patient = patient_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    old_patient = Patient.query.get(new_patient.user.id)
    if old_patient is None:
        return "No patient with that id", HTTPStatus.NOT_FOUND

    new_patient.user_id = new_patient.user.id

    db.session.merge(new_patient)
    db.session.commit()

    out_patient = patient_schema.dump(new_patient)
    return out_patient, HTTPStatus.OK


@api_patient_controller.route("/patients/<int:id>", methods=['DELETE'])
@has_roles(roles=['admin'])
def delete_patient(id: int):
    """
    Deletes a patient with a given id

    :param id: id of Patient in the db to delete
    """

    patient = Patient.query.get(id)
    if patient is None:
        return "No patient with that id", HTTPStatus.NOT_FOUND

    db.session.delete(patient)
    db.session.commit()

    return "Successfully deleted patient", HTTPStatus.OK
