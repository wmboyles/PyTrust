"""
This file contains the state enum

:author William Boyles:
"""

import enum


class State(enum.Enum):
    """
    A state is a large locational area in the United States.
    This enum also includes several locations that are not technically US states
    but represent areas where a signifigant number of Americans live.
    """

    def __new__(cls, *args, **kwargs):
        """
        Provides a non-default way to construct a State.
        """
        value = args[0]  # Gets by first attribute: abbreviation
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, abbreviation, full_name):
        """
        Creates a new State object

        :param abbreviation: two letter state abbreviation
        :param full_name: full state name
        """

        self.abbreviation = abbreviation
        self.full_name = full_name

    ALABAMA = "AL", "Alabama"
    ALASKA = "AK", "Alaska"
    ARIZONA = "AZ", "Arizona"
    ARKANSAS = "AR", "Arkansas"
    CALIFORNIA = "CA", "California"
    COLORADO = "CO", "Colorado"
    CONNECTICUT = "CT", "Connecticut"
    DELEWARE = "DE", "Deleware"
    FLORDIA = "FL", "Florida"
    GEORGIA = "GE", "Georgia"
    HAWAII = "HI", "Hawaii"
    IDAHO = "ID", "Idaho"
    ILLINOIS = "IL", "Illinois"
    INDIANA = "IN", "Indiana"
    IOWA = "IA", "Iowa"
    KANSAS = "KS", "Kansas"
    KENTUCKY = "KY", "Kentucky"
    LOUISIANA = "LA", "Louisiana"
    MAINE = "ME", "Maine"
    MARYLAND = "MD", "Maryland"
    MASSACHUSETTS = "MA", "Massachusetts"
    MICHIGAN = "MI", "Michigan"
    MINNESOTA = "MN", "Minnesota"
    MISSISSIPPI = "MS", "Mississippi"
    MISSOURI = "MO", "Missouri"
    MONTANA = "MT", "Montana"
    NEBRASKA = "NE", "Nebraska"
    NEVADA = "NV", "Nevada"
    NEW_HAMPSHIRE = "NH", "New Hampshire"
    NEW_JERSEY = "NJ", "New Jersey"
    NEW_MEXICO = "NM", "New Mexico"
    NEW_YORK = "NY", "New York"
    NORTH_CAROLINA = "NC", "North Carolina"
    NORTH_DAKOTA = "ND", "North Dakota"
    OHIO = "OH", "Ohio"
    OKLAHOMA = "OK", "Oklahoma"
    OREGON = "OR", "Oregon"
    PENNSYLVANIA = "PA", "Pennsylvania"
    RHODE_ISLAND = "RI", "Rhode Islands"
    SOUTH_CAROLINA = "SC", "South Carolina"
    SOUTH_DAKOTA = "SD", "South Dakota"
    TENNESSEE = "TN", "Tennsessee"
    TEXAS = "TX", "Texas"
    UTAH = "UT", "Utah"
    VERMONT = "VT", "Vermont"
    VIRGINIA = "VA", "Virginia"
    WASHINGTON = "WA", "Washington"
    WEST_VIRGINIA = "WV", "West Virginia"
    WISCONSIN = "WI", "Wisconsin"
    WYOMING = "WY", "Wyoming"
    DISTRICT_OF_COLUMBIA = "DC", "Washington DC"
    AMERICAN_SAMOA = "AS", "American Samoa"
    GUAM = "GU", "Guam"
    NORTHERN_MARIANA_ISLANDS = "MP", "Northern Mariana Islands"
    PUERTO_RICO = "PR", "Puerto Rico"
    US_VIRGIN_ISLANDS = "VI", "US Virgin Islands"
    OTHER = "OT", "Other"
