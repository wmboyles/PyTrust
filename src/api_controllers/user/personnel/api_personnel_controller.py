"""
This file contains API methods that relate to personnel.
This includes CRUD operations on personnel objects.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request, session
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from src.models.persistent.persistent import db
from src.models.persistent.user.personnel.personnel import Personnel, PersonnelSchema
from src.models.persistent.user.user import User, UserSchema
from src.models.enums.user_role.user_role import UserRole
from src.decorators import has_roles

api_personnel_controller = Blueprint(
    "api_personnel_controller",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@api_personnel_controller.route("/personnel/<string:type>", methods=["GET"])
@has_roles(roles=["hcp", "pharmacist"])
def get_all_personnel_by_type(type: str):
    try:
        role = UserRole(type)
    except ValueError:
        return f"{type} is not a valid User Role", HTTPStatus.NOT_FOUND

    all_ids = {user.id for user in User.query.filter(User.role == role).all()}
    all_personnel = Personnel.query.filter(Personnel.user_id in all_ids).all()

    personnel_schema = PersonnelSchema(many=True)
    out = personnel_schema.dump(all_personnel)

    return jsonify(out), HTTPStatus.OK


@api_personnel_controller.route("/personnel/self", methods=["GET"])
@has_roles(roles=["hcp", "pharmacist"])
def get_self_personnel():
    """
    If there is an existing personnel object correspodning to the calling user, return it
    """

    caller_username = session.get("username", None)
    if caller_username is None:
        return "No username in client session", HTTPStatus.NOT_FOUND

    calling_user = User.query.filter(User.username == caller_username).first()
    calling_personnel = Personnel.query.filter(Personnel.user == calling_user).first()
    if calling_personnel is None:
        user_schema = UserSchema()
        out_user = user_schema.dump(calling_user)

        # return user instead of personnel
        return out_user, HTTPStatus.NOT_FOUND

    personnel_schema = PersonnelSchema()
    out_personnel = personnel_schema.dump(calling_personnel)

    return out_personnel, HTTPStatus.OK


@api_personnel_controller.route("/personnel", methods=["POST"])
@has_roles(roles=["hcp", "pharmacist"])
def make_personnel():
    """
    Creates a personnel
    """

    json_data = request.json

    personnel_schema = PersonnelSchema()
    try:
        personnel = personnel_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    user_id = personnel.user.id
    db_user = User.query.get(user_id)
    if db_user is None:
        return "Provided user does not match existing user", HTTPStatus.NOT_FOUND

    # just comparing the user objects doesn't work. Have to look at serialization
    user_schema = UserSchema()
    db_user_json = user_schema.dump(db_user)
    personnel_user_json = user_schema.dump(personnel.user)
    if db_user_json != personnel_user_json:
        return "Provided user's fields do not match stored fields", HTTPStatus.CONFLICT

    db_personnel = Personnel.query.get(user_id)
    if db_personnel is not None:
        return "Already a personnel for this user", HTTPStatus.CONFLICT

    db.session.merge(personnel)
    db.session.commit()

    out_personnel = personnel_schema.dump(personnel)
    return out_personnel, HTTPStatus.OK


@api_personnel_controller.route("/personnel", methods=["PUT"])
@has_roles(roles=["hcp", "pharmacist"])
def edit_personnel():
    """
    Edits an existing personnel
    """

    json_data = request.json

    personnel_schema = PersonnelSchema()
    try:
        new_personnel = personnel_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        print(e)
        return str(e), HTTPStatus.BAD_REQUEST

    old_personnel = Personnel.query.get(new_personnel.user.id)
    if old_personnel is None:
        return "No personnel with that id", HTTPStatus.NOT_FOUND

    new_personnel.user_id = new_personnel.user.id
    # new_personnel.hospital_id = new_personnel.hospital.id
    # new_personnel.pharmacy_id = new_personnel.pharmacy.id

    db.session.merge(new_personnel)
    db.session.commit()

    out_personnel = personnel_schema.dump(new_personnel)
    return out_personnel, HTTPStatus.OK


@api_personnel_controller.route("/personnel/<int:id>", methods=["DELETE"])
@has_roles(roles=["hcp", "pharmacist"])
def delete_personnel(id: int):
    """
    Deletes a personnel with a given id

    :param id: id of Patient in the db to delete
    """

    personnel = Personnel.query.get(id)
    if personnel is None:
        return "No personnel with that id", HTTPStatus.NOT_FOUND

    db.session.delete(personnel)
    db.session.commit()

    return "Successfully deleted personnel", HTTPStatus.OK
