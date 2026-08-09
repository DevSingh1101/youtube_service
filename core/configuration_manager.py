from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigurationManager(BaseSettings):
    app_name: str = "YouTube Automation"

    # Token Environment
    secret_key: str
    encoding_algorithm: str = "HS256"

    # Database Environment
    database_url: str = f"sqlite:///database.db"

    model_config = SettingsConfigDict(env_file=".env")


configuration_manager = ConfigurationManager()