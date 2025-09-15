# TEST-OPS-IA

API for web scraping and testing web applications.

## Container Building
```
# Build the Docker image
docker build -t test-ops-ia .

# Run in detached mode (background)
docker run -d -p 8000:8000 --name test-ops-ia-container test-ops-ia

# Run in foreground
docker run -p 8000:8000 test-ops-ia
```

## Using the API

### Via Swagger UI
- Open: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Test endpoints interactively:
  - `POST /scrape/` → scrape a website  
    Request body example:
    ```
    {
      "url": "https://example.com/",
      "timeout": 10
    }
    ```
  - `GET /scrape/health` → health check  
  - `GET /scrape/screenshot/{url}` → get a website screenshot  

### Via Postman

1. **Scrape a website (POST /scrape/)**  
   URL: `http://localhost:8000/scrape/`  
   Body (JSON):
   ```
   {
     "url": "https://example.com",
     "wait_for": "div.content",
     "timeout": 10
   }
   ```

2. **Get screenshot (GET /scrape/screenshot/{url})**  
   URL: `http://localhost:8000/scrape/screenshot/https://example.com`

3. **Health check (GET /scrape/health)**  
   URL: `http://localhost:8000/scrape/health`

### Notes
- ChromeDriver initializes on the first request.  
- `HEADLESS=True` runs the browser in headless mode.  
- Extracted data includes: title, URL, page length, screenshot (base64), links, and text preview.
