import os
from dotenv import load_dotenv
from loguru import logger


class EnvVariableNotFound(Exception):
    def __init__(self, variable_name: str) -> None:
        super().__init__(f"Environment variable {variable_name} not found in .env file")
        logger.error(f"Environment variable {variable_name} not found in .env file")


class Config:
    def __init__(self) -> None:
        load_dotenv(override=True)

        self._bot_token = self._get_bot_token()
        self._admins = self._get_admins()
        self._configs_prefix = self._get_configs_prefix()
        self._base_subscription_monthly_price_rubles = (
            self._get_base_subscription_monthly_price_rubles()
        )
        self._db_connection_parameters = self._get_db_connection_parameters()
        self._peer_dns = self._get_peer_dns()
        self._yookassa_parameters = self._get_payment_fields()

    @property
    def bot_token(self) -> str:
        return self._bot_token

    @property
    def admins(self) -> list[int]:
        return self._admins

    @property
    def configs_prefix(self) -> str:
        return self._configs_prefix

    @property
    def base_subscription_monthly_price_rubles(self) -> int:
        return self._base_subscription_monthly_price_rubles

    @property
    def db_connection_parameters(self) -> dict:
        return self._db_connection_parameters

    @property
    def peer_dns(self) -> str:
        return self._peer_dns
    
    @property
    def get_yookassa_params(self) -> tuple:
        return self._yookassa_parameters["account_id"], self._yookassa_parameters["secret_key"]

    def _get_bot_token(self) -> str:
        bot_token = os.getenv("WG_BOT_TOKEN")
        if not bot_token:
            raise EnvVariableNotFound("WG_BOT_TOKEN")
        return bot_token

    def _get_admins(self) -> list[int]:
        admins_str = os.getenv("ADMINS_IDS")
        if not admins_str:
            raise EnvVariableNotFound("ADMINS_IDS")
        return list(map(int, [admin for admin in admins_str.split(",") if admin]))

    def _get_configs_prefix(self) -> str:
        configs_prefix = os.getenv("CONFIGS_PREFIX")
        if not configs_prefix:
            raise EnvVariableNotFound("CONFIGS_PREFIX")
        return configs_prefix

    def _get_db_connection_parameters(self) -> dict:
        db_connection_parameters = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_USER_PASSWORD"),
            "database": os.getenv("DATABASE"),
        }
        for key, value in db_connection_parameters.items():
            if not value:
                if key == "password":
                    key = "user_password"
                raise EnvVariableNotFound(
                    f"{'DB_' if key != 'database' else ''}{key.upper()}"
                )
        return db_connection_parameters

    def _get_base_subscription_monthly_price_rubles(self) -> int:
        base_subscription_monthly_price_rubles = os.getenv(
            "BASE_SUBSCRIPTION_MONTHLY_PRICE_RUBLES"
        )
        if not base_subscription_monthly_price_rubles:
            raise EnvVariableNotFound("BASE_SUBSCRIPTION_MONTHLY_PRICE_RUBLES")
        return float(base_subscription_monthly_price_rubles)

    def _get_peer_dns(self) -> str:
        peer_dns = os.getenv("PEER_DNS")
        if not peer_dns:
            raise EnvVariableNotFound("PEER_DNS")
        return peer_dns
    
    def _get_payment_fields(self) -> dict:
        payment_fields = {
            "account_id": os.getenv("Y_ACCOUNT_ID"),
            "secret_key": os.getenv("Y_SECRET_KEY")
        }

        for key, value in payment_fields.items():
            if not value:
                raise EnvVariableNotFound(
                    f"{key.upper()} not found"
                )

        return payment_fields
