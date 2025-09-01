from src.interactor.flow_controller import FlowController
from src.uni_scraper.scraper_processor import ScraperProcessor
from src.uni_scraper.websites import websites
from src.job_model_builder import JobModelFromScraper

class ScraperController:
    def __init__(self):
        self.flow_controller = FlowController()
        self.scraper_processor = ScraperProcessor()

    def scraper(self):
        print("SCRAPER CONTROLLER")
        final_results = []

        for site, url in websites.items():
            try:
                results = []
                scrape = self.scraper_processor.scrape(site, url)

                if not scrape:
                    print(f"Failed to scrape {site}.")
                    continue

                results.extend(scrape if isinstance(scrape, list) else [scrape])

                for job in results:
                    print(f"\nProcessing job: {job['job_fields']}\n")

                    job["job_fields"] = self.flow_controller.run_flow(extract=True, job_fields=job["job_fields"])
                    print(f"Processed job fields: {job['job_fields']}")

                    if hasattr(job["job_fields"], 'to_dict'):
                        job["job_fields"] = job["job_fields"].to_dict()
                        print(f"Job fields after conversion: {job['job_fields']}")

                    job["job_fields"] = self.normalize_job_fields(job["job_fields"])
                    print(f"Normalized job fields: {job['job_fields']}")

                    new_job = JobModelFromScraper(job["job_fields"])
                    final_results.append(
                        {
                            "job_fields": new_job.to_dict(),
                            "information": self.information(job["job_fields"]),
                            "source_link": job["source_link"]
                        }
                    )

                    print(f"results: {results}\n")

            except Exception as e:
                print(f"❌ Error scraping {site}: {str(e)}")
                continue

        return final_results
        
        # return [
#   {
#     "job_fields": {
#       "job_title": "Software Engineer",
#       "company": {"code": "123", "name": "TechCorp"},
#       "work_area": {"code": "IT", "name": "Tecnologias de Informação"},
#       "payment_frequency": {"code": "M", "name": "Mensal"},
#       "type_of_applicant": {"code": "J", "name": "Júnior"},
#       "district": {"code": "13", "name": "Lisboa"},
#       "job_description": "Desenvolvimento de aplicações web em Python e React.",
#       "job_address": "Avenida da Liberdade, Lisboa",
#       "job_country": "Portugal",
#       "job_city": "Lisboa",
#       "work_mode": "On-site",
#       "degree_of_specialization": "Non-specialized",
#       "benefits": "Seguro de saúde, subsídio de alimentação"
#     },
#     "information": "Completo",
#     "source_link": "https://www.net-empregos.com/123456"
#   }
# ]
        

    def normalize_job_fields(self, job_fields):
        default_selects = {
            'company': {'code': '', 'name': 'Não sei'},
            'work_area': {'code': '', 'name': 'Não sei'},
            'payment_frequency': {'code': '', 'name': 'Não sei'},
            'type_of_applicant': {'code': '', 'name': 'Não sei'},
            'district': {'code': '', 'name': 'Não sei'},
        }
        default_texts = {
            'job_title': 'Não sei',
            'job_description': 'Não sei',
            'job_address': 'Não sei',
            'job_country': 'Portugal',
            'job_city': 'Não sei',
            'work_mode': 'On-site',
            'degree_of_specialization': 'Non-specialized',
            'benefits': '',
        }

        for field, default in default_selects.items():
            value = job_fields.get(field, None)
            if not value or (isinstance(value, str) and value.strip() == ''):
                job_fields[field] = default
            elif isinstance(value, str):
                job_fields[field] = {'code': value, 'name': value}
            elif isinstance(value, dict):
                if 'code' not in value or 'name' not in value:
                    job_fields[field] = default

        for field, default in default_texts.items():
            value = job_fields.get(field, None)
            if not value or (isinstance(value, str) and value.strip() == ''):
                job_fields[field] = default

        return job_fields

    def information(self, job_fields):
        if not job_fields:
            return "Incompleto"

        for value in job_fields.values():
            if value == "":
                return "Incompleto"

        return "Completo"
