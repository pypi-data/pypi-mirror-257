from .exceptions import IpAddressFormatError, InvalidSearchAttribute
from abc import ABC, abstractmethod


class MTObject(ABC):
    @abstractmethod
    def get_one(self, find_by: dict):
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def save(self):
        pass

    def _checking_find_by_field(self, find_by: dict) -> bool:
        """Возращает True если все поля поиска существуют для данного объекта.
        Иначе генерируется исключение InvalidSearchAttribute"""
        if not isinstance(find_by, dict):
            raise ValueError("'find_by' must by 'dict'")
        attributes_ls = []
        ex_attributes = ['connection', 'image', 'flags']
        for att in list(vars(self).keys()):
            new_atr = att.replace(rf'_{self.__class__.__name__}__', '', 1)
            if new_atr not in ex_attributes:
                attributes_ls.append(new_atr)
        for field in find_by.keys():
            if field not in attributes_ls:
                raise InvalidSearchAttribute(f'The "{field}" attribute does not exist for the object. \n'
                                             f'Use only {attributes_ls}')
        return True


CIDR = {
    '255.255.255.255': 32, '255.255.255.254': 31, '255.255.255.252': 30, '255.255.255.248': 29,
    '255.255.255.240': 28, '255.255.255.224': 27, '255.255.255.192': 26, '255.255.255.128': 25,
    '255.255.255.0': 24, '255.255.254.0': 23, '255.255.252.0': 22, '255.255.248.0': 21,
    '255.255.240.0': 20, '255.255.224.0': 19, '255.255.192.0': 18, '255.255.128.0': 17,
    '255.255.0.0': 16, '255.254.0.0': 15, '255.252.0.0': 14, '255.248.0.0': 13,
    '255.240.0.0': 12, '255.224.0.0': 11, '255.192.0.0': 10, '255.128.0.0': 9,
    '255.0.0.0': 8, '254.0.0.0': 7, '252.0.0.0': 6, '248.0.0.0': 5,
    '240.0.0.0': 4, '224.0.0.0': 3, '192.0.0.0': 2, '128.0.0.0': 1, '0.0.0.0': 0
}


class IPAddress:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError('Object must be a string')
        self._value = value.strip()
        self.address = None
        self.mask = None
        self.__checking_value()

    def __checking_value(self):
        address_mask = self._value.split('/')
        try:
            if len(address_mask) > 2:
                raise ValueError
            address = address_mask[0].split('.')
            if len(address) != 4:
                raise ValueError
            for a in address:
                _ip = int(a)
                if _ip < 0 or _ip > 255:
                    raise ValueError
            self.address = address_mask[0]
            if len(address_mask) == 2:
                if address_mask[1] in CIDR.keys():
                    self.mask = CIDR[address_mask[1]]
                else:
                    _mask = int(address_mask[1])
                    if _mask in CIDR.values():
                        self.mask = str(address_mask[1])
                    else:
                        raise ValueError
                if self.mask == '0' and self.address != '0.0.0.0':
                    raise IpAddressFormatError('In this case, the subnet mask cannot be 0.')
        except ValueError:
            raise IpAddressFormatError('Invalid IP address format.\n'
                                       'Example: 192.168.32.15/24 or 192.168.32.15/255.255.255.0')

    def __str__(self):
        address = self.address
        if self.mask:
            address += f'/{self.mask}'
        return address


