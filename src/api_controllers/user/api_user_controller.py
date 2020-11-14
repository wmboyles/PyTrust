"""
This file contains API methods that relate to users.
This includes CRUD operations on user objects, as well as related things like
getting a list of all user roles.

:author William Boyles:
"""

from flask import Blueprint, jsonify, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from ...persistent.persistent import db
from ...persistent.user.user import User, UserSchema
from ...persistent.user.user_role import UserRole
from ...decorators import has_roles

api_user_controller = Blueprint("api_user_controller",
                                __name__,
                                template_folder="templates",
                                static_folder="static",
                                url_prefix="/")


@api_user_controller.route("/users", methods=['GET'])
@has_roles(roles=['admin'])
def get_all_users():
    """
    Gets a list of all users in the DB
    """

    all_users = User.query.all()

    user_schema = UserSchema(many=True)
    out_users = user_schema.dump(all_users)

    return jsonify(out_users), HTTPStatus.OK


@api_user_controller.route("/users", methods=['POST'])
@has_roles(roles=['admin'])
def make_user():
    """
    Creates a user
    """

    json_data = request.json
    if 'password' not in json_data:
        return "No password provided", HTTPStatus.BAD_REQUEST

    user_password = json_data['password']
    json_data.pop('password')

    user_schema = UserSchema()
    try:
        user = user_schema.load(json_data)
        user.set_password(user_password)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    db_user = User.query.filter(User.username == user.username).first()
    if db_user:
        return "User with that username already exists", HTTPStatus.CONFLICT

    db.session.add(user)
    db.session.commit()

    out_user = user_schema.dump(user)
    return out_user, HTTPStatus.OK


@api_user_controller.route("/users", methods=['PUT'])
@has_roles(roles=['admin'])
def edit_user():
    """
    Edits an existing user
    """

    json_data = request.json

    user_schema = UserSchema()
    try:
        new_user = user_schema.load(json_data)
    except (AssertionError, ValidationError) as e:
        return str(e), HTTPStatus.BAD_REQUEST

    old_user = User.query.get(new_user.id)
    if old_user is None:
        return "No user with that id", HTTPStatus.NOT_FOUND

    db.session.merge(new_user)
    db.session.commit()

    out_user = user_schema.dump(new_user)
    return out_user, HTTPStatus.OK


@api_user_controller.route("/users/<int:id>", methods=['DELETE'])
@has_roles(roles=['admin'])
def delete_user(id: int):
    """
    Deletes a user with a given id

    :param id: id of User in the db to delete
    """

    user = User.query.get(id)

    if user is None:
        return "No user with that id", HTTPStatus.NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return "Successfully deleted user", HTTPStatus.OK


@api_user_controller.route("/user_roles", methods=['GET'])
@has_roles(roles=['admin'])
def get_all_user_roles():
    """
    Gets a list of all user roles defined in the UserRole enum.
    """

    user_roles = [role.value for role in UserRole]

    return jsonify(user_roles), HTTPStatus.OK