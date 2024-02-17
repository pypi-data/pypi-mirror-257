from src.smart_energy_data_vald3nir.repository.consumption.consumption_dto import *


def to_consumption_json_format(json_list: list[dict]) -> list[dict]:
    return [to_consumption_single_json_format(json) for json in json_list]


def to_consumption_single_json_format(data_json: dict) -> dict:
    return json_to_consumption(data_json).to_json()


def json_to_consumption(data_json: dict) -> ConsumptionDTO:
    return ConsumptionDTO(
        sensor_id=data_json["sensor_id"],
        date=data_json["date"],
        power=data_json["power"]
    )


def to_yearly_consumption_json_format(json_list: list[dict]) -> list[dict]:
    return [
        YearlyConsumptionDTO(
            year=json["year"],
            power=json["power"]
        ).to_json() for json in json_list
    ]


def to_monthly_consumption_json_format(json_list: list[dict]) -> list[dict]:
    return [
        MonthlyConsumptionDTO(
            year=json["year"],
            month=json["month"],
            power=json["power"]
        ).to_json() for json in json_list
    ]


def to_date_consumption_list(json_list: list[dict]) -> list[dict]:
    return [
        DateConsumptionDTO(
            date=json["date"],
            power=json["power"]
        ).to_json() for json in json_list
    ]


#
#
def to_day_night_consumption_list(json_list: list[dict]) -> list[dict]:
    return [
        DayAndNightConsumptionDTO(
            month=json["month"],
            power_day=json["power_day"],
            power_night=json["power_night"]
        ).to_json() for json in json_list
    ]


def to_consumption_duplicated_list(json_list: list[dict]) -> list[ConsumptionDuplicatedDTO]:
    return [
        ConsumptionDuplicatedDTO(
            consumption=json_to_consumption(json["consumption"]),
            ids_duplicated=json["ids_duplicated"]
        ) for json in json_list
    ]
