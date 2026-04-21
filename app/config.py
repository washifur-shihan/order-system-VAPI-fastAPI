from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    VAPI_API_KEY: str
    ELEVENLABS_API_KEY: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()