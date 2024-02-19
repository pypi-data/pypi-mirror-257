from ..datasets import *
from ..datasets.base_dataset import DefaultDataset, JsonDataset
from ..repository.address.address_dao import AddressDAO
from ..repository.address.address_mapper import to_address_json_format
from ..repository.consumption.consumption_dao import EnergyConsumptionDAO
from ..repository.consumption.consumption_mapper import to_consumption_json_format
from ..repository.env_conditions.env_conditions_dao import EnvConditionsDAO
from ..repository.env_conditions.env_conditions_mapper import to_environment_json_format
from ..repository.generation.generation_dao import EnergyGeneratedDAO
from ..repository.generation.generation_mapper import to_energy_generated_json_format
from ..repository.sensor.sensor_dao import SensorDAO
from ..repository.sensor.sensor_mapper import to_sensor_json_format
from ..repository.user.user_dao import UserDAO
from ..repository.user.user_mapper import to_user_json_format


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
