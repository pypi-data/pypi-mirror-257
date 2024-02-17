from src.smart_energy_data_vald3nir.repository.user.user_dto import UserDTO


def to_user_json_format(json_list: list[dict]) -> list[dict]:
    return [
        UserDTO(
            name=json["name"],
            email=json["email"],
            client_id=json["client_id"],
            created_at=json["created_at"],
            my_sensors=json["my_sensors"],
            shared_sensors=json["shared_sensors"]
        ).to_json() for json in json_list
    ]
