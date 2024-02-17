from src.smart_energy_data_vald3nir.repository import BaseDAO
from src.smart_energy_data_vald3nir.repository.generation import EnergyGeneratedRepository


class EnergyGeneratedDAO(BaseDAO, EnergyGeneratedRepository):

    def __init__(self) -> None:
        super().__init__(collection=self._collection_name())

    def list_all(self) -> list[dict]:
        res = self.find_documents(query={})
        return self.mapper.to_energy_generated_json_format(res)

    def list_yearly_generation(self) -> list[dict]:
        res = self.aggregate(self.pipeline.yearly_generation_pipeline())
        return self.mapper.to_yearly_generation_json_format(res)

    def list_monthly_generation(self, year: str, limit: int = 24) -> list[dict]:
        res = self.aggregate(self.pipeline.monthly_generation_pipeline(year, limit))
        return self.mapper.to_monthly_generation_json_format(res)

    def insert_energy_generated(self, data: list[dict]) -> str:
        self.insert_documents(data)
        return f"Inserted {len(data)} documents"

    def delete_energy_generated(self, generation_id: str) -> str:
        _n_documents_deleted = self.delete_documents(query={"generation_id": generation_id})
        return f"Deleted {_n_documents_deleted} documents"
