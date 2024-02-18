from src.smart_energy_data.repository.base_classes import BaseDAO


class AddressDAO(BaseDAO):
    def __init__(self) -> None:
        super().__init__(collection="address")

    # def list_addresses(self) -> list[AddressDTO]:
    #     return self._list_all_objects()
