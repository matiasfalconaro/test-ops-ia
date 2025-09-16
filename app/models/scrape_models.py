from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any, List
from .enums import ExtractType


class ScrapeRequest(BaseModel):
    url: HttpUrl
    wait_for: Optional[str] = None
    timeout: Optional[int] = 10
    save_screenshot: Optional[bool] = False


class ScrapeResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ExtractionRule(BaseModel):
    name: str
    selector: str
    extract: ExtractType = ExtractType.TEXT
    attribute: Optional[str] = None


class CustomScrapeRequest(BaseModel):
    url: HttpUrl
    wait_for: Optional[str] = None
    timeout: Optional[int] = 10
    extract_rules: List[ExtractionRule]
    screenshot: bool = False
    full_page: bool = False
    save_screenshot: Optional[bool] = False


class BatchScrapeRequest(BaseModel):
    requests: List[CustomScrapeRequest]
    parallel: bool = False