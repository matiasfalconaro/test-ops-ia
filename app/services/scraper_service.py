import time
import base64
import os
import re

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional, Dict, List, Any


class SeleniumScraper:

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None
        self.screenshot_dir = os.path.join(os.path.dirname(__file__),
                                           '..',
                                           'screenshots')
        os.makedirs(self.screenshot_dir, exist_ok=True)
    

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
    

    def scrape_website(self,
                       url: str,
                       wait_for: Optional[str] = None,
                       timeout: int = 10,
                       save_screenshot: bool = False) -> Dict[str, Any]:
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
            
            screenshot_data = self.take_screenshot()
            screenshot_path = None
            
            if save_screenshot and screenshot_data:
                screenshot_path = self.save_screenshot_to_file(screenshot_data, url)
            
            page_data = {
                "url": url,
                "title": self.driver.title,
                "current_url": self.driver.current_url,
                "page_source_length": len(self.driver.page_source),
                "screenshot": screenshot_data,
                "screenshot_path": screenshot_path,
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
    

    def save_screenshot_to_file(self,
                                base64_data: str,
                                url: str) -> str:
        """
        Save base64 screenshot to PNG file
        Returns the file path if successful, None otherwise
        """
        try:
            from urllib.parse import urlparse
            import re
            
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('.', '_')
            path = parsed_url.path.replace('/', '_') if parsed_url.path else 'home'
            
            filename = f"{domain}_{path}"[:100]
            filename = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}.png"
            
            filepath = os.path.join(self.screenshot_dir, filename)
            
            image_data = base64.b64decode(base64_data)
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            print(f"Screenshot guardado como PNG en: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error guardando screenshot como PNG: {e}")
            return None
    

    def extract_with_rules(self,
                           rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract data based on custom rules"""
        if not self.driver:
            return {}
        
        extracted_data = {}
        for rule in rules:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, rule['selector'])
                
                if rule['extract'] == 'text':
                    extracted_data[rule['name']] = [element.text for element in elements]
                elif rule['extract'] == 'attribute' and rule.get('attribute'):
                    extracted_data[rule['name']] = [element.get_attribute(rule['attribute']) for element in elements]
                elif rule['extract'] == 'html':
                    extracted_data[rule['name']] = [element.get_attribute("outerHTML") for element in elements]
                    
            except Exception as e:
                extracted_data[rule['name']] = f"Error extracting: {str(e)}"
        
        return extracted_data


    def _get_page_data(self) -> Dict[str, Any]:
        """Internal method to get basic page data (reusable)"""
        return {
            "url": self.driver.current_url if self.driver else "",
            "title": self.driver.title if self.driver else "",
            "current_url": self.driver.current_url if self.driver else "",
            "page_source_length": len(self.driver.page_source) if self.driver else 0,
        }


    def custom_scrape(self,
                      url: str,
                      rules: List[Dict[str, Any]],
                      wait_for: Optional[str] = None, 
                      timeout: int = 10,
                      screenshot: bool = False,
                      full_page: bool = False,
                      save_screenshot: bool = False) -> Dict[str, Any]:
        """Perform custom scraping with specific rules"""
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
            
            extracted_data = self.extract_with_rules(rules)
            
            screenshot_data = None
            screenshot_path = None
            if screenshot:
                screenshot_data = self.take_screenshot()
                if save_screenshot and screenshot_data:
                    screenshot_path = self.save_screenshot_to_file(screenshot_data, url)
            
            result = {
                **self._get_page_data(),
                "extracted_data": extracted_data,
                "status": "success"
            }
            
            if screenshot:
                result["screenshot"] = screenshot_data
                if screenshot_path:
                    result["screenshot_path"] = screenshot_path
            
            if full_page:
                result.update({
                    "links": self.extract_links(),
                    "text_content": self.extract_text_content(),
                    "text_content_preview": self.extract_text_content()[:500] + "..." if self.extract_text_content() else ""
                })
            
            return result
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}


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
