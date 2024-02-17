from src.smart_energy_data_vald3nir.repository.env_conditions.env_conditions_dto import *


def to_environment_dto(json: dict) -> EnvConditionsDTO:
    return EnvConditionsDTO(
        date=json["date"],
        sensor_id=json["sensor_id"],
        temperature=json["temperature"],
        humidity=json["humidity"]
    )


def to_environment_list(json_list: list[dict]) -> list[EnvConditionsDTO]:
    return [to_environment_dto(json) for json in json_list]


def to_environment_json_format(json_list: list[dict]) -> list[dict]:
    return [to_environment_dto(json).to_json() for json in json_list]


def to_environment_duplicated_list(json_list: list[dict]) -> list[EnvConditionsDuplicatedDTO]:
    return [
        EnvConditionsDuplicatedDTO(
            environment=to_environment_dto(json),
            ids_duplicated=json["ids_duplicated"]
        ) for json in json_list
    ]
