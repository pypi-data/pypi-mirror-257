from .utilites import print_color
from functools import wraps
from typing import Callable, TypeVar, ParamSpec


class PyMikroTikExceptions(Exception):
    pass


class ConnectError(PyMikroTikExceptions):
    pass


class IpAddressFormatError(PyMikroTikExceptions):
    pass


class RouterError(PyMikroTikExceptions):
    pass


class InvalidSearchAttribute(PyMikroTikExceptions):
    pass


class SaveError(PyMikroTikExceptions):
    pass


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def exception_control(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if args[0].connection._ignore_errors is False:
            return method(*args, **kwargs)
        try:
            return method(*args, **kwargs)
        except PyMikroTikExceptions as err:
            print_color(str(err), 'red')
            return err
    return wrapper
