"""
This file contains API methods that relate to states.
This includes selected CRUD operations.
"""

from flask import Blueprint, jsonify
from http import HTTPStatus

from ...persistent.state.state import State

api_state_controller = Blueprint("api_state_controller",
                                 __name__,
                                 template_folder="templates",
                                 static_folder="static",
                                 url_prefix="/")


@api_state_controller.route("/states", methods=['GET'])
def get_all_states_short():
    """
    Gets a list of all states defined in the State enum.
    """

    states = [(state.value, state.full_name) for state in State]

    return jsonify(states), HTTPStatus.OK
