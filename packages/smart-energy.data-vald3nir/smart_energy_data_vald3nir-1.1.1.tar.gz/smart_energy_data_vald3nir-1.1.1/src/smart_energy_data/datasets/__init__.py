import os

# ----------------------------------------------------------------------------------------------------------------------
# BASE PATHS
# ----------------------------------------------------------------------------------------------------------------------

_DATASETS_FOLDER = os.path.relpath(os.path.dirname(__file__)) + "/data"

# ----------------------------------------------------------------------------------------------------------------------
# DATASETS
# ----------------------------------------------------------------------------------------------------------------------

USERS_DATASET_PATH = f"{_DATASETS_FOLDER}/users.json"
ADDRESS_DATASET_PATH = f"{_DATASETS_FOLDER}/address.csv"
ENERGY_GENERATED_DATASET_PATH = f"{_DATASETS_FOLDER}/energy_generated.csv"
SENSORS_DATASET_PATH = f"{_DATASETS_FOLDER}/sensors.csv"
ENVIRONMENT_DATASET_PATH = f"{_DATASETS_FOLDER}/environment.csv"
ENERGY_CONSUMPTION_DATASET_PATH = f"{_DATASETS_FOLDER}/energy_consumption.csv"
