from dataclasses import dataclass, asdict

from src.smart_energy_data_vald3nir.libs.keys.smart_energy_secrets import DatabaseEnv
from src.smart_energy_data_vald3nir.libs.toolkit.database.mongodb.mongo_api import MongoAPI
from src.smart_energy_data_vald3nir.libs.toolkit.database.mongodb.mongo_dao import MongoDAO
from src import mongodb_address


# ----------------------------------------------------------------------------------------------------------------------
class BaseApi(MongoAPI):
    def __init__(self, collection: str, print_curl: bool = False) -> None:
        super().__init__(
            api_url=DatabaseEnv.DATABASE_API.value,
            api_key=DatabaseEnv.DATABASE_API_KEY.value,
            database=DatabaseEnv.DATABASE_NAME.value,
            data_source=DatabaseEnv.DATA_SOURCE.value,
            collection=collection,
            print_curl=print_curl
        )


# ----------------------------------------------------------------------------------------------------------------------

class BaseDAO(MongoDAO):

    def __init__(self, collection: str) -> None:
        super().__init__(
            client_url=mongodb_address(),
            project_name=DatabaseEnv.DATABASE_NAME.value,
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
