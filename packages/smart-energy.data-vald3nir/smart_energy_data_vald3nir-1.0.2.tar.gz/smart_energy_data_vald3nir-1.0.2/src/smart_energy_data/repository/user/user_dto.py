from dataclasses import dataclass

from src.smart_energy_data.repository.base_classes import BaseDTO


@dataclass
class UserDTO(BaseDTO):
    name: str
    email: str
    client_id: str
    created_at: str
    my_sensors: list[str]
    shared_sensors: list[str]
