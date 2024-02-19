from dataclasses import dataclass

from smart_energy_data.repository import BaseDTO


@dataclass
class EnvConditionsDTO(BaseDTO):
    date: str
    sensor_id: str
    temperature: float
    humidity: int
