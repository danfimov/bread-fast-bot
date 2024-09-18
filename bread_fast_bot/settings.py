from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str = ''

    model_config = SettingsConfigDict(env_file="conf/.env")


_settings: Settings | None = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


__all__ = [
    "Settings",
    "get_settings",
]
