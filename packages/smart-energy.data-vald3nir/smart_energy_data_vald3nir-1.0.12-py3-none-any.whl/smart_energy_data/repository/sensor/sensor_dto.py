from dataclasses import dataclass

from src.smart_energy_data.repository import BaseDTO


@dataclass
class SensorDTO(BaseDTO):
    alias: str
    sensor_id: str
    created_at: str
    address_id: str
