from .router_objects import MTObject, IPAddress
from .utilites import print_color
import re


class PPPInterface(MTObject):
    def __init__(self, connection):
        self.connection = connection

    def get_all(self) -> list:
        pass

    def get_one(self, find_by: dict):
        pass

    def save(self):
        pass


class PPP:
    def __init__(self, connection):
        self.connection = connection

    @property
    def interface(self):
        interface = PPPInterface(connection=self.connection)
        return interface


