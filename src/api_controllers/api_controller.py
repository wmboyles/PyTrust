"""
This file essentially list all the api blueprints and saves them in a
collection that can be imported by the main app. This is meant to cut down on
the number of imports in the main app and make it easier to add and remove
apis.
"""

from .drug import api_drug_controller as drug
from .user import api_user_controller as user

# All api prefixes begin with /api
BASE_URL = "/api"

# Collection of blueprints
blueprints = {
    drug.api_drug_controller,
    user.api_user_controller,
}