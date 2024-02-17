import src.smart_energy_data_vald3nir.repository.generation.generation_mapper as mapper
import src.smart_energy_data_vald3nir.repository.generation.generation_pipeline as pipeline


class EnergyGeneratedRepository:

    def __init__(self):
        super().__init__()
        self.mapper = mapper
        self.pipeline = pipeline

    def _collection_name(self):
        return "energy_generated"

    def list_all(self) -> list[dict]:
        pass

    def list_yearly_generation(self) -> list[dict]:
        pass

    def list_monthly_generation(self, year: str, limit: int = 24) -> list[dict]:
        pass

    def insert_energy_generated(self, data: list[dict]) -> str:
        pass

    def delete_energy_generated(self, generation_id: str) -> str:
        pass
