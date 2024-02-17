from dataclasses import dataclass

from bson import ObjectId

from src.smart_energy_data_vald3nir.repository import BaseDTO


@dataclass
class ConsumptionDTO(BaseDTO):
    sensor_id: str
    date: str
    power: float


@dataclass
class ConsumptionDuplicatedDTO(BaseDTO):
    consumption: ConsumptionDTO
    ids_duplicated: list[ObjectId]

    def objects_ids_duplicated(self) -> list[ObjectId]:
        return [ObjectId(oid) for oid in self.ids_duplicated]

    def to_consumption_json(self) -> dict:
        return self.consumption.to_json()


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
