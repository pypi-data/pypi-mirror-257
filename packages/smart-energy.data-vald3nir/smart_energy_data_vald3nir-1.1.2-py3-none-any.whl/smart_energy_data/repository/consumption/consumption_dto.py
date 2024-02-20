from dataclasses import dataclass

from ...repository import BaseDTO


@dataclass
class ConsumptionDTO(BaseDTO):
    sensor_id: str
    date: str
    power: float


@dataclass
class DateConsumptionDTO(BaseDTO):
    date: str
    power: float


@dataclass
class DayAndNightConsumptionDTO(BaseDTO):
    month: str
    power_day: float
    power_night: float


@dataclass
class MonthlyConsumptionDTO(BaseDTO):
    year: str
    month: str
    power: float


@dataclass
class YearlyConsumptionDTO(BaseDTO):
    year: str
    power: float
