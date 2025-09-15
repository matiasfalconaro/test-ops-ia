from fastapi import (APIRouter,
                     HTTPException)
from pydantic import (BaseModel,
                      HttpUrl)
from typing import Optional, Dict, Any
from app.services.scraper_service import scraper


router = APIRouter(prefix="/scrape", tags=["scraping"])


class ScrapeRequest(BaseModel):
    url: HttpUrl
    wait_for: Optional[str] = None
    timeout: Optional[int] = 10


class ScrapeResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/", response_model=ScrapeResponse)
async def scrape_website(request: ScrapeRequest):
    """
    Scrape a website using Selenium
    
    - **url**: Website URL to scrape
    - **wait_for**: CSS selector to wait for before scraping (optional)
    - **timeout**: Timeout in seconds (default: 10)
    """
    try:
        result = scraper.scrape_website(
            url=str(request.url),
            wait_for=request.wait_for,
            timeout=request.timeout
        )
        
        if "error" in result:
            return ScrapeResponse(success=False, error=result["error"])
        
        return ScrapeResponse(success=True, data=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "selenium-scraper"}


@router.get("/screenshot/{url:path}")
async def get_screenshot(url: str):
    """Get screenshot of a website"""
    try:
        result = scraper.scrape_website(url=url)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "screenshot": result.get("screenshot"),
            "title": result.get("title")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
