from .router_objects import MTObject, IPAddress
from .exceptions import exception_control, RouterError, InvalidSearchAttribute, SaveError
from .utilites import print_color
import re


class Address(MTObject):
    """
    Address managemen
    /ip address (object)
    """
    def __init__(self, connection):
        self.connection = connection
        self.__address: IPAddress | None = None
        self.__network: IPAddress | None = None
        self.interface: str | None = None
        self.comment: str | None = None
        self.numbers: int | None = None
        self.disabled: bool | None = None
        self.flags: str | None = None
        self.__image: dict = {}

    @property
    def address(self) -> IPAddress | None:
        return self.__address

    @address.setter
    def address(self, value: str | IPAddress | None):
        if isinstance(value, IPAddress) or value is None:
            self.__address = value
        else:
            self.__address = IPAddress(value)

    @property
    def network(self) -> IPAddress | None:
        return self.__network

    @network.setter
    def network(self, value: str | IPAddress | None):
        if isinstance(value, IPAddress) or value is None:
            self.__network = value
        else:
            self.__network = IPAddress(value)

    @exception_control
    def add(self, address: str, interface: str, network: str = None,
            comment: str = None, disabled: bool = False) -> 'Address':
        """
        Create a new item

        :param address: Local IP address
        :param interface: Interface name
        :param network: Network
        :param comment: Short description of the item
        :param disabled: Disable items
        :return: 'Address'
        """
        address = address if isinstance(address, IPAddress) else IPAddress(address)
        command = f'/ip address add address="{str(address)}" interface="{interface}"'
        if network:
            network = network if isinstance(network, IPAddress) else IPAddress(network)
            command += f' network="{str(network)}"'
        command += f' comment="{comment}"' if comment else ''
        command += f' disabled="yes"' if disabled is True else ''

        number_address = len(self.get_all())

        result = self.connection.send_command(command)
        if result:
            raise RouterError(result)
        added_address = self.get_all()[number_address]
        print_color(f"IP address '{added_address.address}' added to interface '{added_address.interface}'", 'cyan')
        return added_address

    @exception_control
    def set(self, find_by: dict or int, address: str = None, interface: str = None,
            network: str = None, disabled: bool = None, comment: str = None) -> 'Address':
        """
        Change item properties

        :param find_by: Either a dictionary or an integer indicating how to look up the IP address.
                        If it is a dictionary, it must contain key-value pairs for identifying the IP address.
                        If it is an integer, it represents a number from a list of IP addresses.
        :param address: Local IP address
        :param interface: Interface name
        :param network: Network
        :param disabled: Disable items
        :param comment: Short description of the item
        :return: 'Address'
        """
        edit_address = self.get_one(find_by=find_by)

        if address:
            edit_address.address = IPAddress(address)
        if interface:
            edit_address.interface = interface
        if network:
            edit_address.network = IPAddress(network)
        if disabled:
            edit_address.disabled = disabled
        if comment:
            edit_address.comment = comment
        edit_address.save()

        print_color('IP address parameters changed', 'cyan')
        return edit_address

    def disable(self, numbers: int) -> 'Address':
        """
        Disable items

        :param numbers: List of item numbers
        :return: 'Address'
        """
        address = self.__functions('disable', numbers)
        print_color(f'IP address {str(address.address)} disabled', 'cyan')
        return address

    def enable(self, numbers: int):
        """
        Enable items

        :param numbers: List of item numbers
        :return: 'Address'
        """
        address = self.__functions('enable', numbers)
        print_color(f'IP address {str(address)} enabled', 'cyan')
        return address

    def remove(self, numbers: int):
        """
        Remove item

        :param numbers: List of item numbers
        :return: 'Address'
        """
        address = self.__functions('remove', numbers)
        print_color(f'IP address deleted', 'cyan')
        return address

    def get_all(self) -> list['Address']:
        """
        Get all items

        :return: list['Address']
        """
        command = '/ip address print detail'
        result = self.connection.send_command(command)
        pattern = re.compile(r'\s*(\d+)\s+([DIX]?)\s*(?:\s*;;; (.*?))?\s*address=([0-9./]+)\s+network=([0-9.]+)\s+interface=([^\s]+)')
        addresses_string = pattern.findall(result)

        addresses: list[Address] = []
        for _address in addresses_string:
            _index, flag, comment, address, network, interface = _address
            addresses.append(self.__create_an_object(_index, flag, comment, address, network, interface))
        return addresses

    def get_one(self, find_by: dict or int):
        """
        Get one items

        :param find_by: Either a dictionary or an integer indicating how to look up the IP address.
                        If it is a dictionary, it must contain key-value pairs for identifying the IP address.
                        If it is an integer, it represents a number from a list of IP addresses.
        """
        if isinstance(find_by, dict) and find_by.get('numbers'):
            find_by = find_by.get('numbers')
        if isinstance(find_by, int):
            try:
                item = self.get_all()[find_by]
                return item
            except IndexError:
                raise InvalidSearchAttribute('Not find')
        else:
            self._checking_find_by_field(find_by)
            command = '/ip address print detail where '
            for k, v in find_by.items():
                if v:
                    command += f'{k}="{v}" '
            result = self.connection.send_command(command)
            pattern = re.compile(
                r'\s*(\d+)\s+([DIX]?)\s*(?:\s*;;; (.*?))?\s*address=([0-9./]+)\s+network=([0-9.]+)\s+interface=([^\s]+)')
            try:
                address_ = pattern.findall(result)[0]
            except IndexError:
                raise InvalidSearchAttribute('Not find')
            get_address = self.__create_an_object(*address_)
            image = get_address.__image
            del image['numbers']
            addresses = self.get_all()
            for address in addresses:
                s_image = address.__image.copy()
                del s_image['numbers']
                if image == s_image:
                    return address
            raise InvalidSearchAttribute('Not find')

    def print_all(self) -> str:
        """
        Print out all items

        :return: String listing all items
        """
        addresses = self.get_all()
        text = ''
        for address in addresses:
            text += f'\n{str(address)}'
        print_color(text, 'cyan')
        return text

    def save(self, copy: bool = False):
        if copy is True or self.numbers is None:
            new_address = self.add(
                address=self.address,
                interface=self.interface,
                network=self.network,
                comment=self.comment,
                disabled=self.disabled
            )
            return new_address
        if self.__check_image() is not True:
            raise SaveError('The object cannot be saved because it was previously'
                            ' modified or deleted by another application.')
        command = f'/ip address set {self.numbers}'
        attributes = ['address', 'interface', 'network', 'comment', 'disabled']
        for k, v in vars(self).items():
            if k in attributes:
                if k == 'disabled':
                    v = 'yes' if v is True else 'no'
                command += f' {k}="{str(v)}"'
        result = self.connection.send_command(command)
        if result:
            raise RouterError(result)
        saved_address = self.get_one(self.numbers)
        for k, v in vars(saved_address).items():
            setattr(self, k, v)
        return self

    def __create_an_object(self, _index, flag, comment, address, network, interface):
        ip_address = Address(connection=self.connection)
        ip_address.address = IPAddress(address)
        ip_address.network = IPAddress(network)
        ip_address.interface = interface
        ip_address.numbers = int(_index)
        ip_address.flags = flag if flag else ''
        ip_address.disabled = True if flag == 'X' else False
        if comment:
            ip_address.comment = comment
        ip_address.__set_image()
        return ip_address

    def __functions(self, func: str, numbers: int) -> 'Address' or None:
        addresses = self.get_all()
        addresses_numbers = [address.numbers for address in addresses]
        if numbers not in addresses_numbers:
            raise InvalidSearchAttribute(f'There is no number {numbers} in the address list.\n'
                                         f'Here is a list of available numbers\n'
                                         f'{addresses_numbers}')
        command = f'/ip address {func} {numbers}'
        result = self.connection.send_command(command)
        if result:
            raise RouterError(result)
        if func == 'remove':
            return None
        return self.get_all()[numbers]

    def __set_image(self):
        img = vars(self)
        ex_attributes = ['connection', 'flags', '_Address__image']
        self.__image = {k: str(v) for k, v in img.items() if k not in ex_attributes}

    def __check_image(self) -> bool:
        address = self.get_one({'numbers': self.numbers})
        if address.__image == self.__image:
            return True
        return False

    def __str__(self):
        st = f'{self.numbers} ' if self.numbers is not None else ''
        st += f'{self.flags} address={self.address} network={self.network} interface={self.interface}'
        if self.comment:
            st += f' comment={self.comment}'
        return st


class Ip:
    def __init__(self, connection):
        self.connection = connection

    @property
    def address(self):
        address = Address(connection=self.connection)
        return address
