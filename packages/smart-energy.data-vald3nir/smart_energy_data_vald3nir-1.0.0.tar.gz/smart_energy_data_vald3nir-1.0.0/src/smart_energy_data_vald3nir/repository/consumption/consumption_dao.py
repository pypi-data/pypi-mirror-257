from src.smart_energy_data_vald3nir.repository import BaseDAO
from src.smart_energy_data_vald3nir.repository.consumption import EnergyConsumptionRepository


class EnergyConsumptionDAO(BaseDAO, EnergyConsumptionRepository):

    def __init__(self) -> None:
        super().__init__(collection=self._collection_name())

    def get_all_consumption(self, sensor_id: str, limit: int = 10000) -> list[dict]:
        res = self.find_documents(query={"sensor_id": sensor_id}, limit=limit)
        return self.mapper.to_consumption_json_format(res)

    def get_yearly_consumption(self, sensor_id: str) -> list[dict]:
        res = self._db.aggregate(pipeline=self.pipeline.yearly_consumption_pipeline(sensor_id))
        return self.mapper.to_yearly_consumption_json_format(res)

    def get_monthly_consumption(self, sensor_id: str, n_months: int = 12) -> list[dict]:
        res = self._db.aggregate(pipeline=self.pipeline.monthly_consumption_pipeline(sensor_id, n_months))
        return self.mapper.to_monthly_consumption_json_format(res)

    def get_monthly_consumption_by_year(self, sensor_id: str, year: str) -> list[dict]:
        res = self._db.aggregate(pipeline=self.pipeline.monthly_consumption_by_year_pipeline(sensor_id, year))
        return self.mapper.to_monthly_consumption_json_format(res)

    def get_daily_consumption(self, sensor_id: str, n_days: int) -> list[dict]:
        res = self._db.aggregate(pipeline=self.pipeline.daily_consumption_pipeline(sensor_id, n_days))
        return self.mapper.to_date_consumption_list(res)

    def get_daily_consumption_details(self, sensor_id: str, date: str) -> list[dict]:
        res = self._db.aggregate(pipeline=self.pipeline.daily_consumption_details_pipeline(sensor_id, date))
        return self.mapper.to_date_consumption_list(res)

    def get_last_hours_consumption(self, sensor_id: str, n_hours: int) -> list[dict]:
        res = self._db.aggregate(pipeline=self.pipeline.last_hours_consumption_pipeline(sensor_id, n_hours))
        return self.mapper.to_date_consumption_list(res)

    def get_day_and_night_consumption(self, sensor_id: str, n_months: int = 12) -> list[dict]:
        res = self._db.aggregate(pipeline=self.pipeline.day_and_night_consumption_pipeline(sensor_id, n_months))
        return self.mapper.to_day_night_consumption_list(res)

    # ------------------------------------------------------------------------------------------------------
    # TIME SERIES
    # ------------------------------------------------------------------------------------------------------

    def remove_duplicates(self):
        data_array = self._db.aggregate(pipeline=self.pipeline.sum_consumption_day_duplicated_pipeline())
        for data in self.mapper.to_consumption_duplicated_list(data_array):
            if len(data.ids_duplicated) > 1:
                self.delete_objects(data.objects_ids_duplicated())
                self.insert_document(data.to_consumption_json())
