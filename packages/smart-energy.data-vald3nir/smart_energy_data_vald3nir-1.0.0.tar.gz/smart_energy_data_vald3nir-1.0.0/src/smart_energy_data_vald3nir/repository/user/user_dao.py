from src.smart_energy_data_vald3nir.repository import BaseDAO


class UserDAO(BaseDAO):
    def __init__(self) -> None:
        super().__init__(collection="users")

    # def check_client_existed(self, email) -> bool:
    #     return self._db.find_one(query={"email": email})
    #
    # def insert_one(self, client: ClientDTO):
    #     if self.check_client_existed(client.email):
    #         raise Exception(f"Email {client.email} já cadastrado.")
    #     self._db.insert_one(client.to_json())
    #
    # def update_one(self, client: ClientDTO):
    #     self._db.update_one(
    #         query={"email": client.email},
    #         values=client.to_json()
    #     )
