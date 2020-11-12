"""
Contains function decorators used throughout the project.

:author William Boyles:
"""

from http import HTTPStatus
from flask import session
from functools import wraps

DEFAULT_RETURN_IF_FAIL = ("User not authorized", HTTPStatus.UNAUTHORIZED)


def has_roles(roles, return_if_fail=DEFAULT_RETURN_IF_FAIL):
    """
    Ensures that user is logged in as someone with a given role.
    
    :param roles: List of authorized role names
    :param return_if_fail: What to return if user not authorized
    """
    def role_wrapper(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if session.get('role') in roles:
                return func(*args, **kwargs)
            else:
                return return_if_fail

        return func_wrapper

    return role_wrapper