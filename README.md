# TEST-OPS-IA

API for web scraping and testing web applications.

## Container management
```bash
chmod +x docker.sh
./ docker.sh --help
```

## Using the API

### Via Swagger UI
- Open: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Test endpoints interactively:
  - `POST /scrape/` → scrape a website  
    Request body example:
    ```json
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
   ```json
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
