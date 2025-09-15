import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import (Optional,
                    Dict,
                    List,
                    Any)


class SeleniumScraper:

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
    

    def init_driver(self):
        """Initialize Chrome WebDriver for Linux"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
        
        chrome_options.binary_location = "/usr/bin/google-chrome-stable"
        
        try:
            self.driver = webdriver.Chrome(
                service=Service("/usr/bin/chromedriver"),
                options=chrome_options
            )
        except Exception as e:
            print(f"ChromeDriver initialization failed: {e}")
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
                raise Exception(f"Failed to initialize ChromeDriver: {fallback_error}")
        
        return self.driver
    

    def scrape_website(self, url: str, wait_for: Optional[str] = None, timeout: int = 10) -> Dict[str, Any]:
        """Scrape a website and return page content"""
        if not self.driver:
            self.init_driver()
        
        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)
            
            if wait_for:
                print(f"Waiting for element: {wait_for}")
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, wait_for))
                )
            else:
                print("Waiting for page load...")
                time.sleep(3)
            
            page_data = {
                "url": url,
                "title": self.driver.title,
                "current_url": self.driver.current_url,
                "page_source_length": len(self.driver.page_source),
                "screenshot": self.take_screenshot(),
                "links_count": len(self.extract_links()),
                "text_content_preview": self.extract_text_content()[:500] + "..." if self.extract_text_content() else "",
                "status": "success"
            }
            
            return page_data
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    

    def extract_links(self) -> List[Dict[str, str]]:
        """Extract all links from the page"""
        if not self.driver:
            return []
        
        links = []
        try:
            anchor_tags = self.driver.find_elements(By.TAG_NAME, "a")
            for tag in anchor_tags:
                href = tag.get_attribute("href")
                text = tag.text.strip()
                if href and href.startswith(('http://', 'https://')):
                    links.append({"text": text, "url": href})
        except Exception as e:
            print(f"Error extracting links: {e}")
        
        return links
    

    def extract_text_content(self) -> str:
        """Extract main text content from the page"""
        if not self.driver:
            return ""
        
        try:
            # Get body text
            body = self.driver.find_element(By.TAG_NAME, "body")
            return body.text.strip()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    

    def take_screenshot(self) -> str:
        """Take screenshot and return as base64"""
        if not self.driver:
            return ""
        
        try:
            return self.driver.get_screenshot_as_base64()
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return ""
    

    def close(self):
        """Close the WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            finally:
                self.driver = None


scraper = SeleniumScraper(headless=True)
