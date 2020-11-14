"""
This file contains the User db model and marshmallow schema.

:author William Boyles:
"""

from marshmallow.decorators import post_load
from marshmallow_enum import EnumField
from werkzeug.security import generate_password_hash, check_password_hash

from ..persistent import db, ma
from .user_role import UserRole


class User(db.Model):
    """
    A User is an account in the system. They have some login credentials and a
    role that defines what they can see and what API methods they can access.

    :param id: Unique id in the database. Is set automatically.
    :param username: Username to login to the system. Must be unique.
    :param password: :assword to login to the system. 6 <= len <= 255.
    :param role: Role in the system.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    # Although this field is required, we set it a bit differently b/c hashing
    password_hash = db.Column(db.String(255))
    role = db.Column(db.Enum(UserRole), nullable=False)
    '''
    We want password to not ever be None, and we have length restrictions
    because we didn't specify this in the column definition, we need to
    explitly check for None, type, and length. We wouldn't normally have to do
    this, but hashing passwords are a bit unique.
    '''
    def set_password(self, password: str) -> None:
        if not password:
            raise AssertionError("No password provided")
        if type(password) is not str:
            raise AssertionError("Password must be a string")
        if len(password) < 6 or len(password) > 255:
            raise AssertionError(
                "Password must be between 6 and 255 characters")

        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    The user schema helps with the serialization and deserializaton of users.
    """
    class Meta:
        include_fk = True
        model = User

    @post_load
    def make_user(self, data: dict, **kwargs) -> User:
        """
        This method is called when calling a load. It transforms a dictionary
        representing the object into the object itself.

        :param data: Dict data representing user object
        """

        return User(**data)

    # Enums have to be done a bit more explicitly to serialize correctly
    role = EnumField(UserRole, by_value=True)
