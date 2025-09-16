from fastapi import APIRouter, HTTPException
from app.services.scraper_service import scraper
from app.models import (ScrapeRequest,
                        ScrapeResponse,
                        CustomScrapeRequest,
                        BatchScrapeRequest)


router = APIRouter(prefix="/scrape", tags=["scraping"])


@router.post("/", response_model=ScrapeResponse)
async def scrape_website(request: ScrapeRequest):
    """
    Scrape a website using Selenium
    
    - **url**: Website URL to scrape
    - **wait_for**: CSS selector to wait for before scraping (optional)
    - **timeout**: Timeout in seconds (default: 10)
    - **save_screenshot**: Whether to save screenshot as PNG file
    """
    try:
        result = scraper.scrape_website(
            url=str(request.url),
            wait_for=request.wait_for,
            timeout=request.timeout,
            save_screenshot=request.save_screenshot
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


@router.post("/custom/", response_model=ScrapeResponse)
async def custom_scrape(request: CustomScrapeRequest):
    """
    Scrape a website with custom extraction rules

    - **extract_rules**: List of rules defining what to extract
    - **screenshot**: Whether to include screenshot
    - **full_page**: Whether to include full page data
    - **save_screenshot**: Whether to save screenshot as PNG file
    """
    try:
        rules_dict = [rule.dict() for rule in request.extract_rules]
        
        result = scraper.custom_scrape(
            url=str(request.url),
            rules=rules_dict,
            wait_for=request.wait_for,
            timeout=request.timeout,
            screenshot=request.screenshot,
            full_page=request.full_page,
            save_screenshot=request.save_screenshot
        )
        
        if "error" in result:
            return ScrapeResponse(success=False, error=result["error"])
        
        return ScrapeResponse(success=True, data=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch/")
async def batch_scrape(request: BatchScrapeRequest):
    """Execute multiple custom scrape requests"""
    results = []
    
    for scrape_request in request.requests:
        try:
            rules_dict = [rule.dict() for rule in scrape_request.extract_rules]
            
            result = scraper.custom_scrape(
                url=str(scrape_request.url),
                rules=rules_dict,
                wait_for=scrape_request.wait_for,
                timeout=scrape_request.timeout,
                screenshot=scrape_request.screenshot,
                full_page=scrape_request.full_page,
                save_screenshot=scrape_request.save_screenshot
            )
            
            results.append({
                "url": str(scrape_request.url),
                "success": "error" not in result,
                "data": result
            })
            
        except Exception as e:
            results.append({
                "url": str(scrape_request.url),
                "success": False,
                "error": str(e)
            })
    
    return {
        "results": results,
        "total": len(results),
        "successful": sum(1 for r in results if r["success"])
    }
