"""
This file simply imports all the persistence class models. It's used the
persisent.py to initialize all the tables in the db while cutting down on
imports.
"""

from .drug import drug
from .user import user