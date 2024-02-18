from dataclasses import dataclass, asdict

from toolkit.database.mongodb.mongo_api import MongoAPI
from toolkit.database.mongodb.mongo_dao import MongoDAO

from src.smart_energy_data.env import DatabaseEnv, mongodb_address


# ----------------------------------------------------------------------------------------------------------------------
class BaseApi(MongoAPI):
    def __init__(self, collection: str, print_curl: bool = False) -> None:
        super().__init__(
            api_url=DatabaseEnv.DATABASE_API.value,
            api_key=DatabaseEnv.DATABASE_API_KEY.value,
            database="smart_energy",
            data_source=DatabaseEnv.DATA_SOURCE.value,
            collection=collection,
            print_curl=print_curl
        )


# ----------------------------------------------------------------------------------------------------------------------

class BaseDAO(MongoDAO):

    def __init__(self, collection: str, database: str = "smart_energy") -> None:
        super().__init__(
            client_url=mongodb_address(),
            project_name=database,
            collection=collection,
        )

    def get_all(self) -> list[dict]:
        return self.find_documents()


# ----------------------------------------------------------------------------------------------------------------------

@dataclass
class BaseDTO:

    def to_json(self) -> dict:
        return asdict(self)

# ----------------------------------------------------------------------------------------------------------------------
