from pydantic_settings import BaseSettings, SettingsConfigDict

base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore"
)

class LLMSettings(BaseSettings):
    GOOGLE_API_KEY: str
    GOOGLE_MODEL: str

    model_config = base_config

llm_settings = LLMSettings()