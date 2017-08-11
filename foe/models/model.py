
"""
"""

# Native
import uuid
from collections import OrderedDict

# 3rd-Party
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr, has_inherited_table

# Proprietary

from request import Request

Base = declarative_base()

# http://docs.sqlalchemy.org/en/latest/orm/versioning.html

def uuid4_hex():
    """
    Return the hex value of the UUID to get rid of '-'
    Also might make serialization faster (native string)
    """

    # TODO: Move to utils?
    return uuid.uuid4().hex[:16]

class Model(Base):
    """
    """

    __abstract__ = True

    REQUEST_CLASS = None

    # Attributes
    # ---------------------------------------------------------

    #

    # Back-refs
    # ---------------------------------------------------------

    # Containers
    # ---------------------------------------------------------

    # Builtins
    # ---------------------------------------------------------

    def __repr__(self):
        """
        """

        return "%s %s" % (self.__class__.__name__.title(), self.id)

    def __init__(self, *args, **kwargs):
        """
        """

        return super(Model, self).__init__(*args, **kwargs)

    # Properties
    # ---------------------------------------------------------

    @declared_attr
    def __tablename__(cls):
        """
        """

        if has_inherited_table(cls):
            return None

        return cls.__name__.lower()

    @property
    def session(self):
        """
        """

        return inspect(self).session

    # Methods
    # ---------------------------------------------------------

    def populate(self, *args, **kwargs):
        """
        """

        for key, value in kwargs.iteritems():

            if key in ['__class__']:
                continue

            setattr(self, key, value)

        return self

    def update(self, *args, **kwargs):
        """
        """

        return self.populate(*args, **kwargs)

    @classmethod
    def request(cls, method, data, klass=None):
        """
        """

        # body = "[{\"__class__\":\"ServerRequest\",\"requestId\":14,\"requestClass\":\"CityProductionService\",\"requestData\":[[223]],\"requestMethod\":\"pickupProduction\",\"voClassName\":\"ServerRequest\"}]"

        klass = klass or cls.REQUEST_CLASS

        payload = [OrderedDict([
            ("requestId", Request.REQUEST_ID),
            ("__class__", "ServerRequest"),
            ("requestClass", klass),
            ("requestData", data),
            ("requestMethod", method),
            ("voClassName", "ServerRequest")]
        )]

        response = Request.request(payload)

        return response
