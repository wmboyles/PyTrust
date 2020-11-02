from flask import Blueprint, jsonify, request
from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from ...persistent.persistent import db
from ...persistent.user.user import User, UserSchema
from ...persistent.user.user_role import UserRole

api_user_controller = Blueprint("api_user_controller",
                                __name__,
                                template_folder="templates",
                                static_folder="static",
                                url_prefix="/")


@api_user_controller.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()

    user_schema = UserSchema(many=True)
    out_users = user_schema.dump(all_users)

    return jsonify(out_users), HTTPStatus.OK


@api_user_controller.route("/users", methods=["POST"])
def make_user():
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


@api_user_controller.route("/user_roles", methods=["GET"])
def get_all_user_roles():
    user_roles = [role.value for role in UserRole]

    return jsonify(user_roles), HTTPStatus.OK