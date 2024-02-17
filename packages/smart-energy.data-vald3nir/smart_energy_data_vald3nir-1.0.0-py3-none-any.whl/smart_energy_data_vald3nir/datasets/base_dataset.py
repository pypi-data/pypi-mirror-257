import src.smart_energy_data_vald3nir.libs.toolkit.utils.backup_utils as backup_utils
from src.smart_energy_data_vald3nir.libs.toolkit.utils.dataset_utils import count_lines
from src.smart_energy_data_vald3nir.repository import BaseDAO


class BaseDataset:

    def __init__(self, dataset_path: str, dao: BaseDAO) -> None:
        super().__init__()
        self.dataset_path = dataset_path
        self.dao = dao

    def get_all(self) -> list[dict]:
        return self.dao.get_all()

    def clear(self):
        return self.dao.clear()

    def restore_from_csv(self):
        self.dao.clear()
        self.dao.insert_documents(self.read_from_csv())

    def restore_from_json(self):
        self.dao.clear()
        self.dao.insert_documents(self.read_from_json())

    def backup_to_json(self, data: list[dict]):
        backup_utils.save_list_to_json(self.dataset_path, data)

    def backup_to_csv(self, data: list[dict]):
        backup_utils.save_list_to_csv(self.dataset_path, data)

    def read_from_json(self) -> list[dict]:
        return backup_utils.load_list_from_json(self.dataset_path)

    def read_from_csv(self):
        return backup_utils.load_list_from_csv(self.dataset_path)

    def dataset_size(self) -> int:
        return count_lines(self.dataset_path)


# ----------------------------------------------------------------------------------------------------------------------
# Types of Datasets
# ----------------------------------------------------------------------------------------------------------------------

class JsonDataset(BaseDataset):
    def __init__(self, dataset_path: str, dao: BaseDAO, json_format):
        super().__init__(dataset_path=dataset_path, dao=dao)
        self.data_format = json_format

    def backup(self):
        self.backup_to_json(self.data_format(self.get_all()))

    def restore(self):
        self.restore_from_json()


class DefaultDataset(BaseDataset):
    def __init__(self, dataset_path: str, dao: BaseDAO, json_format):
        super().__init__(dataset_path=dataset_path, dao=dao)
        self.data_format = json_format

    def backup(self):
        self.backup_to_csv(self.data_format(self.get_all()))

    def restore(self):
        self.restore_from_csv()
