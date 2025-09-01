from src.job_modeler import JobModelFromBot, JobModelFromScraper

class JobModelBuilder:
    def build_from_bot(self, job_fields):
        try:
            return JobModelFromBot(job_fields)
        except Exception as e:
            print(f"❌ Erro ao criar modelo de trabalho (bot): {str(e)}")
            return None

    def build_from_scraper(self, scraped_data):
        try:
            return JobModelFromScraper(scraped_data)
        except Exception as e:
            print(f"❌ Erro ao criar modelo de trabalho (scraper): {str(e)}")
            return None
