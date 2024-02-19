from dataclasses import dataclass

from ...repository import BaseDTO


@dataclass
class AddressDTO(BaseDTO):
    address_id: str
    street: str
    number: int
    complement: str
    district: str
    city: str
    CEP: str
