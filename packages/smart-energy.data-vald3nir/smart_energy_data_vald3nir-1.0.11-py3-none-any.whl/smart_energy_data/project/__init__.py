from src.smart_energy_data.project.secret import DatabaseEnv


# ----------------------------------------------------------------------------------------------------------------------
# Database Environments
# ----------------------------------------------------------------------------------------------------------------------


class _DatabaseEnvironment:

    def __init__(self) -> None:
        self.mongodb_address = DatabaseEnv.DATABASE_ADDRESS_DEBUG.value

    def use_prod(self) -> None:
        self.mongodb_address = DatabaseEnv.DATABASE_ADDRESS_PROD.value


# ----------------------------------------------------------------------------------------------------------------------
# Singleton instances
# ----------------------------------------------------------------------------------------------------------------------

_databaseEnv = _DatabaseEnvironment()


# ----------------------------------------------------------------------------------------------------------------------

def mongodb_address() -> str:
    return _databaseEnv.mongodb_address


def use_mongodb_prod_environment():
    _databaseEnv.use_prod()
