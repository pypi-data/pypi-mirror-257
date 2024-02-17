import time

from src import use_mongodb_prod_environment
from src.smart_energy_data_vald3nir.datasets.datasets import *


def _datasets():
    return [
        AddressDataset(),
        ConsumptionDataset(),
        GenerationDataset(),
        EnvConditionsDataset(),
        SensorDataset(),
        UserDataset()
    ]


def prod_mode():
    use_mongodb_prod_environment()


def backup():
    start = time.time()
    for dataset in _datasets():
        dataset.backup()
    end = time.time()
    print(f"Backup finished: {end - start}")


def restore():
    start = time.time()
    for dataset in _datasets():
        dataset.restore()
    end = time.time()
    print(f"Restore finished: {end - start}")


def update_generation():
    start = time.time()
    GenerationDataset().restore()
    end = time.time()
    print(f"Update finished: {end - start}")


if __name__ == '__main__':
    # prod_mode()
    backup()
    # restore()
