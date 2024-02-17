from src.smart_energy_data_vald3nir.repository import BaseDAO
from src.smart_energy_data_vald3nir.repository.env_conditions import EnvConditionsRepository
from src.smart_energy_data_vald3nir.repository.env_conditions.env_conditions_dto import *


class EnvConditionsDAO(BaseDAO, EnvConditionsRepository):

    def __init__(self) -> None:
        super().__init__(collection=self._collection_name())

    def get_all_objects(self, sensor_id: str) -> list[EnvConditionsDTO]:
        res = self.find_documents(query={"sensor_id": sensor_id})
        return self.mapper.to_environment_list(res)

    def load_environment_last_hours(self, sensor_id: str, n_hours: int) -> list[dict]:
        res = self.find_documents(query={"sensor_id": sensor_id}, sort_field='date', limit=n_hours)
        return self.mapper.to_environment_json_format(res)

    # ------------------------------------------------------------------------------------------------------
    # TIME SERIES
    # ------------------------------------------------------------------------------------------------------

    def remove_duplicates(self):
        res = self.aggregate(pipeline=self.pipeline.avg_environment_duplicated_pipeline())
        data_duplicated: list[EnvConditionsDuplicatedDTO] = self.mapper.to_environment_duplicated_list(res)
        for d in data_duplicated:
            if len(d.ids_duplicated) > 1:
                self.delete_objects(d.objects_ids_duplicated())
                self.insert_document(d.to_environment_json())
