from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "FastAPI Selenium Scraper"
    debug: bool = Field(default=False, env="DEBUG")
    headless: bool = Field(default=True, env="HEADLESS")
    
    class Config:
        env_file = ".env"


settings = Settings()
