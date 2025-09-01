import os
import json
import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from src.interactor.flow_controller import FlowController

logger = logging.getLogger(__name__)

class ScraperProcessor:
    def __init__(self, headless=True):        
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )

    def scrape(self, site: str, url: str):
        print(f"Scraping {site} from {url}...")

        match site:
            case "net-empregos":
                scraper = ScraperNetEmpregos(url)
                return scraper.scrape()
            case _:
                print(f"Site {site} não implementado.")
                return None


logger = logging.getLogger(__name__)

class ScraperNetEmpregos:
    def __init__(self, base_url, cookies_path=None):
        self.USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/113.0.1774.50 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'
        ]
        
        self.base_url = base_url
        self.cookies_path = cookies_path or os.path.join(os.path.dirname(__file__), "cookies_net_empregos.json")
        self.driver = self.create_driver()
        self.flow_controller = FlowController()
    
    def create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={random.choice(self.USER_AGENTS)}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def load_cookies(self):
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, "r", encoding="utf-8") as f:
                for cookie in json.load(f):
                    self.driver.add_cookie(cookie)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=4, max=10))
    def safe_get(self, url):
        self.driver.get(url)
        time.sleep(random.uniform(3, 7))
        return self.driver.page_source

    def parse_listing_page(self):
        listing_url = f"{self.base_url}/pesquisa-empregos.asp?chaves=&cidade=&categoria=0&zona=0&tipo=0"
        html = self.safe_get(listing_url)
        self.load_cookies()
        html = self.safe_get(listing_url)

        soup = BeautifulSoup(html, "html.parser")
        job_cards = soup.find_all("div", class_="job-item job-item-destaque media")
        offers = []
        for card in job_cards:
            try:
                if hasattr(card, "find"):
                    a_tag = card.find('a') # type: ignore
                    href = a_tag.get('href', None) if a_tag else None # type: ignore
                    if href and not href.startswith('http'): # type: ignore
                        href = f"{self.base_url}{href}"
                    offers.append({"link": href})
            except Exception as e:
                logger.warning(f"Erro a extrair link: {e}")
                
        return offers

    def parse_offer_page(self, link):
        html = self.safe_get(link)
        soup = BeautifulSoup(html, "html.parser")
        job_title = soup.find("h1", class_="title")
        job_location = soup.find("a", class_="oferta-link")
        job_description = soup.find("div", class_="job-description mb-40 dont-break-out")

        description = f"""
        Título: {job_title.text.strip() if job_title else ''}
        Localização: {job_location.text.strip() if job_location else ''}
        Descrição: {job_description.text.strip() if job_description else ''}
        """

        return {
            "job_fields": self.flow_controller.extract_job_fields(description),
            "source_link": link
        }

    def scrape(self):
        try:
            offers = self.parse_listing_page()
            for offer in offers:
                if offer.get("link"):
                    return [self.parse_offer_page(offer["link"])]
            return []
        finally:
            self.close_driver()
