"""
This file simply imports all the persistence class models. It's used the
persisent.py to initialize all the tables in the db while cutting down on
imports.

:author William Boyles:
"""

from .drug import drug

from .user import user
from .user.patient import patient
from .user.personnel import personnel

from .institution.pharmacy import pharmacy
from .institution.hospital import hospital