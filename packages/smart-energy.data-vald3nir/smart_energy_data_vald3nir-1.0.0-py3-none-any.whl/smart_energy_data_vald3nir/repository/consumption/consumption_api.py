from src.smart_energy_data_vald3nir.repository import BaseApi
from src.smart_energy_data_vald3nir.repository.consumption import EnergyConsumptionRepository


class EnergyConsumptionAPI(BaseApi, EnergyConsumptionRepository):

    def __init__(self, print_curl: bool = False) -> None:
        super().__init__(collection=self._collection_name(), print_curl=print_curl)

    def get_all_consumption(self, sensor_id: str, limit: int = 10000) -> list[dict]:
        res = self.find_documents(query={"sensor_id": sensor_id}, sort={'_id': 1}, limit=limit)
        return self.mapper.to_consumption_json_format(res)

    def get_yearly_consumption(self, sensor_id: str) -> list[dict]:
        res = self.aggregate(pipeline=self.pipeline.yearly_consumption_pipeline(sensor_id))
        return self.mapper.to_yearly_consumption_json_format(res)

    def get_monthly_consumption(self, sensor_id: str, n_months: int = 12) -> list[dict]:
        res = self.aggregate(pipeline=self.pipeline.monthly_consumption_pipeline(sensor_id, n_months))
        return self.mapper.to_monthly_consumption_json_format(res)

    def get_monthly_consumption_by_year(self, sensor_id: str, year: str) -> list[dict]:
        res = self.aggregate(pipeline=self.pipeline.monthly_consumption_by_year_pipeline(sensor_id, year))
        return self.mapper.to_monthly_consumption_json_format(res)

    def get_daily_consumption(self, sensor_id: str, n_days: int) -> list[dict]:
        res = self.aggregate(pipeline=self.pipeline.daily_consumption_pipeline(sensor_id, n_days))
        return self.mapper.to_date_consumption_list(res)

    def get_daily_consumption_details(self, sensor_id: str, date: str) -> list[dict]:
        res = self.aggregate(pipeline=self.pipeline.daily_consumption_details_pipeline(sensor_id, date))
        return self.mapper.to_date_consumption_list(res)

    def get_last_hours_consumption(self, sensor_id: str, n_hours: int) -> list[dict]:
        res = self.aggregate(pipeline=self.pipeline.last_hours_consumption_pipeline(sensor_id, n_hours))
        return self.mapper.to_date_consumption_list(res)

    def get_day_and_night_consumption(self, sensor_id: str, n_months: int = 12) -> list[dict]:
        res = self.aggregate(pipeline=self.pipeline.day_and_night_consumption_pipeline(sensor_id, n_months))
        return self.mapper.to_day_night_consumption_list(res)
