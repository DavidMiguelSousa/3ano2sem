from src.interactor.flow_controller import FlowController
from src.interactor.scraper_controller import ScraperController

class BotController:
    def __init__(self):
        self.flow_controller = FlowController()
        self.scraper_controller = ScraperController()

    def extract_job(self, description):
        try:
            job_fields = self.flow_controller.run_flow(description=description, extract=True)
            return job_fields

        except Exception as e:
            print(f"❌ Erro ao processar o trabalho: {str(e)}")
            return None

    def scrape_jobs(self):
        scraped_data = self.scraper_controller.scraper()

        if scraped_data and len(scraped_data) > 0:
            print("Scraping completed successfully.")
            return scraped_data
        else:
            print("Scraping failed.")
            return None
