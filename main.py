from fastapi import FastAPI
from app.core.config import settings
from app.routes.scraper import router as scraper_router
from app.services.scraper_service import scraper
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FastAPI Selenium Scraper starting...")
    yield
    scraper.close()
    print("👋 Selenium scraper closed")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)


app.include_router(scraper_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Selenium Scraper API",
        "docs": "/docs",
        "status": "Service ready - ChromeDriver will initialize on first request"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,
                host="0.0.0.0",
                port=8000)
