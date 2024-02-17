from src.smart_energy_data_vald3nir.repository import BaseDAO


class SensorDAO(BaseDAO):
    def __init__(self) -> None:
        super().__init__(collection="sensors")

    # def list_sensors(self) -> list[SensorDTO]:
    #     return self._list_all_objects()
    #
    # def get_sensor(self, sensor_id: str) -> SensorDTO:
    #     try:
    #         return SensorDTO.from_dict(self._db.find_one({"sensor_id": sensor_id}))
    #     except:
    #         print("Not found:", sensor_id)
    #
    # def load_sensors_ids(self) -> list[str]:
    #     return self._db.distinct("sensor_id")
