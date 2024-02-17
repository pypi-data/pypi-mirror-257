from src.smart_energy_data_vald3nir.repository import BaseApi
from src.smart_energy_data_vald3nir.repository.env_conditions import EnvConditionsRepository


class EnvConditionsAPI(BaseApi, EnvConditionsRepository):

    def __init__(self, print_curl: bool = False) -> None:
        super().__init__(collection=self._collection_name(), print_curl=print_curl)

    def load_environment_last_hours(self, sensor_id: str, n_hours: int) -> list[dict]:
        res = self.find_documents(query={"sensor_id": sensor_id}, sort={'date': -1}, limit=n_hours)
        return self.mapper.to_environment_json_format(res)
