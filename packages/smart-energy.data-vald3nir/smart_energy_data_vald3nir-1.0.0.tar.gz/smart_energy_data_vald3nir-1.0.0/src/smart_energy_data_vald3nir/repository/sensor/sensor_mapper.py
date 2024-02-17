from src.smart_energy_data_vald3nir.repository.sensor.sensor_dto import SensorDTO


def to_sensor_json_format(json_list: list[dict]) -> list[dict]:
    return [
        SensorDTO(
            sensor_id=json["sensor_id"],
            address_id=json["address_id"],
            created_at=json["created_at"],
            alias=json["alias"],
        ).to_json() for json in json_list
    ]
