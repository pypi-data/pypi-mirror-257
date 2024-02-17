from src.smart_energy_data_vald3nir.datasets import *
from src.smart_energy_data_vald3nir.datasets.base_dataset import DefaultDataset, JsonDataset
from src.smart_energy_data_vald3nir.repository.address.address_dao import AddressDAO
from src.smart_energy_data_vald3nir.repository.address.address_mapper import to_address_json_format
from src.smart_energy_data_vald3nir.repository.consumption.consumption_dao import EnergyConsumptionDAO
from src.smart_energy_data_vald3nir.repository.consumption.consumption_mapper import to_consumption_json_format
from src.smart_energy_data_vald3nir.repository.env_conditions.env_conditions_dao import EnvConditionsDAO
from src.smart_energy_data_vald3nir.repository.env_conditions.env_conditions_mapper import to_environment_json_format
from src.smart_energy_data_vald3nir.repository.generation.generation_dao import EnergyGeneratedDAO
from src.smart_energy_data_vald3nir.repository.generation.generation_mapper import to_energy_generated_json_format
from src.smart_energy_data_vald3nir.repository.sensor.sensor_dao import SensorDAO
from src.smart_energy_data_vald3nir.repository.sensor.sensor_mapper import to_sensor_json_format
from src.smart_energy_data_vald3nir.repository.user.user_dao import UserDAO
from src.smart_energy_data_vald3nir.repository.user.user_mapper import to_user_json_format


class AddressDataset(DefaultDataset):
    def __init__(self) -> None:
        super().__init__(
            dataset_path=ADDRESS_DATASET_PATH,
            dao=AddressDAO(),
            json_format=to_address_json_format
        )


class ConsumptionDataset(DefaultDataset):
    def __init__(self) -> None:
        super().__init__(
            dataset_path=ENERGY_CONSUMPTION_DATASET_PATH,
            dao=EnergyConsumptionDAO(),
            json_format=to_consumption_json_format
        )


class GenerationDataset(DefaultDataset):
    def __init__(self) -> None:
        super().__init__(
            dataset_path=ENERGY_GENERATED_DATASET_PATH,
            dao=EnergyGeneratedDAO(),
            json_format=to_energy_generated_json_format
        )


class EnvConditionsDataset(DefaultDataset):
    def __init__(self) -> None:
        super().__init__(
            dataset_path=ENVIRONMENT_DATASET_PATH,
            dao=EnvConditionsDAO(),
            json_format=to_environment_json_format
        )


class SensorDataset(DefaultDataset):
    def __init__(self) -> None:
        super().__init__(
            dataset_path=SENSORS_DATASET_PATH,
            dao=SensorDAO(),
            json_format=to_sensor_json_format
        )


class UserDataset(JsonDataset):
    def __init__(self) -> None:
        super().__init__(
            dataset_path=USERS_DATASET_PATH,
            dao=UserDAO(),
            json_format=to_user_json_format
        )
