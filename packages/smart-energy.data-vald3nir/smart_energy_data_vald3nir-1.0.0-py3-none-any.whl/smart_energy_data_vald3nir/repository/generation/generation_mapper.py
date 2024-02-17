from src.smart_energy_data_vald3nir.repository.generation.generation_dto import *


def to_energy_generated_dto(json: dict) -> EnergyGeneratedDTO:
    return EnergyGeneratedDTO(
        generation_id=json["generation_id"],
        date=json["date"],
        power=json["power"]
    )


def to_yearly_generation_dto(json: dict) -> YearlyGenerationDTO:
    return YearlyGenerationDTO(
        year=json["year"],
        power=json["power"]
    )


def to_monthly_generation_dto(json: dict) -> MonthlyGenerationDTO:
    return MonthlyGenerationDTO(
        month=json["month"],
        power=json["power"]
    )


def to_energy_generated_list(json_list: list[dict]) -> list[EnergyGeneratedDTO]:
    return [to_energy_generated_dto(json) for json in json_list]


def to_energy_generated_json_format(json_list: list[dict]) -> list[dict]:
    return [to_energy_generated_dto(json).to_json() for json in json_list]


def to_yearly_generation_json_format(json_list: list[dict]) -> list[dict]:
    return [to_yearly_generation_dto(json).to_json() for json in json_list]


def to_monthly_generation_json_format(json_list: list[dict]) -> list[dict]:
    return [to_monthly_generation_dto(json).to_json() for json in json_list]
