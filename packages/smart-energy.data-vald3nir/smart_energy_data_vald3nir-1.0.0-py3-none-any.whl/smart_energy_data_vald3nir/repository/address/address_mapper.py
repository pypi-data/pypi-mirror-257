from src.smart_energy_data_vald3nir.repository.address.address_dto import AddressDTO


def to_address_json_format(json_list: list[dict]) -> list[dict]:
    return [
        AddressDTO(
            address_id=json["address_id"],
            CEP=json["CEP"],
            city=json["city"],
            district=json["district"],
            street=json["street"],
            number=json["number"],
            complement=json["complement"],
        ).to_json() for json in json_list
    ]
