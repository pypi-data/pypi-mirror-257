from smart_energy_data.repository import BaseDAO
from smart_energy_data.repository.env_conditions import EnvConditionsRepository
from smart_energy_data.repository.env_conditions.env_conditions_dto import EnvConditionsDTO


class EnvConditionsDAO(BaseDAO, EnvConditionsRepository):

    def __init__(self) -> None:
        super().__init__(collection=self._collection_name())

    def get_all_objects(self, sensor_id: str) -> list[EnvConditionsDTO]:
        res = self.find_documents(query={"sensor_id": sensor_id})
        return self.mapper.to_environment_list(res)

    def load_environment_last_hours(self, sensor_id: str, n_hours: int) -> list[dict]:
        res = self.find_documents(query={"sensor_id": sensor_id}, sort_field='date', limit=n_hours)
        return self.mapper.to_environment_json_format(res)
