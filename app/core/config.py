from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from functools import cached_property

class Settings(BaseSettings):
    app_name: str = "Selenium Scraper API"
    debug: bool = Field(default=False, env="DEBUG")
    headless: bool = Field(default=True, env="HEADLESS")
    
    @cached_property
    def version(self) -> str:
        """
        Reads the version from the version.txt file in the root directory.
        """
        project_root = Path(__file__).parent.parent.parent
        version_file_path = project_root / "version.txt"
        
        try:
            return version_file_path.read_text().strip()
        except FileNotFoundError:
            return "0.1.0" 
    
    class Config:
        env_file = ".env"

settings = Settings()