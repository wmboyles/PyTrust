"""
This file imports and contains a collection of all api controllers that relate to enums.
This file exists to cut down on the number of import statements in the main api_controller.py file

:author William Boyles:
"""

from .blood_type.api_blood_type_controller import api_blood_type_controller
from .drug_type.api_drug_type_controller import api_drug_type_controller
from .ethnicity.api_ethnicity_controller import api_ethnicity_controller
from .gender.api_gender_controller import api_gender_controller
from .state.api_state_controller import api_state_controller
from .user_role.api_user_role_controller import api_user_role_controller

api_enum_controllers = {
    api_blood_type_controller,
    api_drug_type_controller,
    api_ethnicity_controller,
    api_gender_controller,
    api_state_controller,
    api_user_role_controller,
}