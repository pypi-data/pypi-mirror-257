import src.smart_energy_data_vald3nir.repository.consumption.consumption_mapper as mapper
import src.smart_energy_data_vald3nir.repository.consumption.consumption_pipeline as pipeline


class EnergyConsumptionRepository:

    def __init__(self):
        super().__init__()
        self.mapper = mapper
        self.pipeline = pipeline

    def _collection_name(self):
        return "energy_consumption"

    # ------------------------------------------------------------------------------------------------------------------
    #  Use cases
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_consumption(self, sensor_id: str, limit: int = 10000) -> list[dict]:
        pass

    def get_yearly_consumption(self, sensor_id: str) -> list[dict]:
        pass

    def get_monthly_consumption(self, sensor_id: str, n_months: int = 12) -> list[dict]:
        pass

    def get_monthly_consumption_by_year(self, sensor_id: str, year: str) -> list[dict]:
        pass

    def get_daily_consumption(self, sensor_id: str, n_days: int) -> list[dict]:
        pass

    def get_daily_consumption_details(self, sensor_id: str, date: str) -> list[dict]:
        pass

    def get_last_hours_consumption(self, sensor_id: str, n_hours: int) -> list[dict]:
        pass

    def get_day_and_night_consumption(self, sensor_id: str, n_months: int = 12) -> list[dict]:
        pass
