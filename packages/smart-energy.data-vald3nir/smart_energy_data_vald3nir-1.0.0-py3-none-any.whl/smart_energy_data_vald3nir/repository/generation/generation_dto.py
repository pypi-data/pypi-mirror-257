from dataclasses import dataclass

from src.smart_energy_data_vald3nir.repository import BaseDTO


@dataclass
class EnergyGeneratedDTO(BaseDTO):
    generation_id: str
    date: str
    power: float


@dataclass
class YearlyGenerationDTO(BaseDTO):
    year: str
    power: float


@dataclass
class MonthlyGenerationDTO(BaseDTO):
    month: str
    power: float
