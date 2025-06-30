from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)  
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(env_path))

    agent_api_key: str
    domain_api_base_url: AnyUrl
    log_level: str = "INFO"

settings = Settings()
