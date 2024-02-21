from .router_objects import MTObject, IPAddress
from .utilites import print_color
import re


class Interface(MTObject):

    def get_all(self) -> list:
        pass

    def get_one(self, find_by: dict):
        pass


