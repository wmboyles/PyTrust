"""
This file generates sample data in the database

:author William Boyles:
"""

from .persistent import db

from .user.user_role import UserRole
from .user.user import User

# Password used when generating sample users
DEFAULT_PASSWORD = "password"


def generate_sample_data():
    """
    Drop exiting tables, recreate them, and generate sample data
    """
    db.drop_all()
    db.create_all()
    _generate_sample_users()


def _generate_sample_users():
    """
    Generate some sample users. One per user role.
    Username will be their role name and password will be default.
    """

    for role in UserRole:
        user = User()
        user.username = role.value
        user.role = role
        user.set_password(DEFAULT_PASSWORD)

        db.session.add(user)

    db.session.commit()