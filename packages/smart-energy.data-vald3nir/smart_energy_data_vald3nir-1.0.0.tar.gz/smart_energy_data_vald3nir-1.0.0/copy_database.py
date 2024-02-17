import time

from src.smart_energy_data_vald3nir.libs.toolkit.database.mongodb.mongo_dao import copy_databases
from src import DatabaseEnv

if __name__ == '__main__':
    start = time.time()
    copy_databases(
        # DATABASE NAMES
        origin_database_name=DatabaseEnv.DATABASE_NAME,
        origin_database_address=DatabaseEnv.DATABASE_ADDRESS_PROD,
        # DATABASE ADDRESSES
        destination_database_name=DatabaseEnv.DATABASE_NAME,
        destination_database_address=DatabaseEnv.DATABASE_ADDRESS_DEBUG
    )
    end = time.time()
    print(f"Copy finished: {end - start}")
