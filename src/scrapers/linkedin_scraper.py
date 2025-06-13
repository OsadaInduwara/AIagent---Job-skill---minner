import time
import urllib.parse
import random
from typing import List, Dict, Optional
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from ..config.job_keywords import JobKeywords


class LinkedInScraper:
    def __init__(self):
        self.driver = None

    def _setup_chrome_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            return True

        except Exception as e:
            print(f"Failed to setup Chrome driver: {e}")
            return False

    def search_jobs_for_keyword(self, keyword: str, location: str, date_filter: str) -> List[Dict]:
        if not self._setup_chrome_driver():
            return []

        jobs = []

        try:
            search_url = self._build_linkedin_url(keyword, location, date_filter)

            self.driver.get(search_url)
            time.sleep(random.uniform(3, 5))

            job_cards = self._find_job_cards()

            for i, card in enumerate(job_cards[:5]):
                job_data = self._extract_job_info(card, keyword)
                if job_data:
                    jobs.append(job_data)

                time.sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"Error scraping jobs for '{keyword}': {e}")

        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

        return jobs

    def _build_linkedin_url(self, keyword: str, location: str, date_filter: str) -> str:
        base_url = "https://www.linkedin.com/jobs/search/"
        date_param = JobKeywords.get_date_filter(date_filter)

        keyword_encoded = urllib.parse.quote_plus(keyword)
        location_encoded = urllib.parse.quote_plus(location)

        url = f"{base_url}?keywords={keyword_encoded}&location={location_encoded}&f_TPR={date_param}"
        return url

    def _find_job_cards(self) -> List:
        job_cards = []

        selectors = [
            ".job-search-card",
            ".base-search-card",
            "[data-view-name='job-card']",
            ".jobs-search__results-list li"
        ]

        for selector in selectors:
            try:
                WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if job_cards:
                    break
            except:
                continue

        return job_cards

    def _extract_job_info(self, card, search_keyword: str) -> Optional[Dict]:
        try:
            title = self._extract_text_with_selectors(card, [
                "h3.base-search-card__title a",
                ".base-search-card__title a",
                "h3 a",
                "h3"
            ])

            company = self._extract_text_with_selectors(card, [
                "h4.base-search-card__subtitle a",
                ".base-search-card__subtitle a",
                "h4"
            ])

            location = self._extract_text_with_selectors(card, [
                ".job-search-card__location",
                ".base-search-card__metadata span",
                "[data-test='job-location']"
            ])

            if title and company and location:
                return {
                    "title": title,
                    "company": company,
                    "location": location,
                    "search_keyword": search_keyword,
                    "scraped_at": datetime.now().isoformat(),
                    "source": "LinkedIn"
                }

            return None

        except Exception as e:
            return None

    def _extract_text_with_selectors(self, element, selectors: List[str]) -> Optional[str]:
        for selector in selectors:
            try:
                elem = element.find_element(By.CSS_SELECTOR, selector)
                text = elem.get_attribute("title") or elem.text.strip()
                if text and len(text) > 2:
                    return text
            except:
                continue
        return None