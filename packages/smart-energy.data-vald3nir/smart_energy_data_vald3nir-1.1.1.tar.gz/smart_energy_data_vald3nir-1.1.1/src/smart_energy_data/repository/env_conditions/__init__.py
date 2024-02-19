import smart_energy_data.repository.env_conditions.env_conditions_mapper as mapper


class EnvConditionsRepository:

    def __init__(self):
        super().__init__()
        self.mapper = mapper

    def _collection_name(self):
        return "environmental_conditions"

    def load_environment_last_hours(self, sensor_id: str, n_hours: int) -> list[dict]:
        pass
