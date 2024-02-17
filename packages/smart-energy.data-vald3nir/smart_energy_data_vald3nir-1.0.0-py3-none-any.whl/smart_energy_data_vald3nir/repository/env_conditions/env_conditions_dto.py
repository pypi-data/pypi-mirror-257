from dataclasses import dataclass

from bson import ObjectId

from src.smart_energy_data_vald3nir.repository import BaseDTO


@dataclass
class EnvConditionsDTO(BaseDTO):
    date: str
    sensor_id: str
    temperature: float
    humidity: int


@dataclass
class EnvConditionsDuplicatedDTO(BaseDTO):
    environment: EnvConditionsDTO
    ids_duplicated: list[ObjectId]

    def objects_ids_duplicated(self) -> list[ObjectId]:
        return [ObjectId(oid) for oid in self.ids_duplicated]

    def to_environment_json(self) -> dict:
        return self.environment.to_json()
