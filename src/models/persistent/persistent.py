"""
This file initializes the SQLAlchemy and Marshmallow objects
It imports from a models module that contains imports of all the persistence 
classes.

:author William Boyles:
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# These imports must be below the db and ma declarations to avoid circular import
from .drug import drug
from .user import user
from .user.patient import patient
from .user.personnel import personnel
from .institution.pharmacy import pharmacy
from .institution.hospital import hospital
from .prescription import prescription