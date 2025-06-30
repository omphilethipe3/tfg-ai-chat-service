from pathlib import Path
from dotenv import load_dotenv

# 1) Build an absolute path to your .env and force‐load it
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)  # now os.environ has your real values

# 2) Only after loading the .env do we import Pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl

class Settings(BaseSettings):
    # 3) Point Pydantic at the exact same file
    model_config = SettingsConfigDict(env_file=str(env_path))

    agent_api_key: str
    domain_api_base_url: AnyUrl
    log_level: str = "INFO"

settings = Settings()
