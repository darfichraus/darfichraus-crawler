from _ctypes_test import func
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
from time import mktime

import jsonpickle as jsonpickle


class JsonEnumHandler(jsonpickle.handlers.BaseHandler):

    def restore(self, obj):
        pass

    def flatten(self, obj: Enum, data):
        return obj.name


class Areal(Enum):
    ZIP = "ZIP",
    COUNTY = "COUNTY",
    STATE = "STATE",
    COUNTRY = "COUNTRY"


class RestrictionType(Enum):
    PUBLIC_TRANSPORTATION = "PUBLIC_TRANSPORTATION",
    EVENTS_AND_ASSEMBLIES = "EVENTS_AND_ASSEMBLIES",
    GASTRONOMY = "GASTRONOMY",
    PUBLIC_PLACES = "PUBLIC_PLACES",
    RETAIL = "RETAIL",
    CURFEW = "CURFEW"


class RestrictionState(Enum):
    BAN = "BAN",
    RESTRICTION = "RESTRICTION"


@dataclass
class Restriction:
    areal: Areal
    arealIdentifier: str
    shortDescription: str
    restrictionDescription: str
    restrictionStart: date
    restrictionEnd: date
    publisher: str
    furtherInformation: str
    restrictionState: RestrictionState = RestrictionState.BAN
    restrictionType: RestrictionType = RestrictionType.EVENTS_AND_ASSEMBLIES
    recipient: str = "Bürger"

    def to_json(self):
        jsonpickle.handlers.registry.register(Enum, JsonEnumHandler, True)
        return jsonpickle.loads(jsonpickle.encode(self, unpicklable=False))


class Mapper:

    def __init__(self, areal, arealIdentifier, adjuster: func = None, use_system_time=False):
        self.use_system_time = use_system_time
        self.adjuster = adjuster
        self.arealIdentifier = arealIdentifier
        self.areal = areal

    def map_to_restriction(self, feedelement: object) -> Restriction:
        if self.use_system_time:
            feedelement.published_parsed = date.today()
        else:
            feedelement.published_parsed = date.fromtimestamp(mktime(feedelement.published_parsed))

        constructed_restriction = Restriction(areal=self.areal, arealIdentifier=self.arealIdentifier,
                                              shortDescription=feedelement.title,
                                              restrictionDescription=feedelement.summary,
                                              restrictionStart=feedelement.published_parsed,
                                              restrictionEnd=(feedelement.published_parsed + timedelta(days=14)),
                                              publisher=self.arealIdentifier, furtherInformation=feedelement.link)

        if self.adjuster:
            constructed_restriction = self.adjuster.__call__(constructed_restriction, feedelement)

        return constructed_restriction
