from src.job_model_builder import JobModelBuilder
from src.uni_bot.protected_thread import start_forms_threads_extract, start_forms_threads_validate
from src.uni_bot.data_processor import DataProcessor
import threading

class FlowController:
    def __init__(self):
        self.lock = threading.Lock()
        self.builder = JobModelBuilder()
        self.processor = DataProcessor()

    def run_flow(self, description=None, job_fields=None, extract=False, create_nlp_model=False, create_scraper_model=False):
        print("FLOW CONTROLLER")

        try:
            if extract:
                if description:
                    data = self.extract_job_fields(description)
                    print("Job fields extracted:\n", data)

                    if data:
                        valid_data = self.validate_fields(data)

                        if not valid_data:
                            print("Job fields validation failed.")
                            return {}
                    
                        print("Job fields validated:\n", valid_data)
                        
                        fix_data = self.fix_job_fields(valid_data)
                        if not fix_data:
                            print("Job fields fixing failed.")
                            return {}

                        print("Job fields fixed:\n", fix_data)

                        return self.run_flow(job_fields=fix_data, create_nlp_model=True)

                elif job_fields:
                    valid_data = self.validate_fields(job_fields)

                    if not valid_data:
                        print("Job fields validation failed.")
                        return {}

                    print("Job fields validated:\n", valid_data)
                    return self.run_flow(job_fields=valid_data, create_nlp_model=True)

            if job_fields:
                if create_nlp_model:
                    try:
                        print("Creating job model...")
                        job_model = self.builder.build_from_bot(job_fields)
                        if not job_model:
                            print("❌ Error: Could not create job model")
                            return None
                        return job_model
                    except Exception as e:
                        print(f"❌ Error creating job model: {str(e)}")
                        return None

                if create_scraper_model:
                    try:
                        print("Creating scraper model...")
                        scraper_model = self.builder.build_from_scraper(job_fields)
                        if not scraper_model:
                            print("❌ Error: Could not create scraper model")
                            return None
                        return scraper_model
                    except Exception as e:
                        print(f"❌ Error creating scraper model: {str(e)}")
                        return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    def extract_job_fields(self, description):
        print("Extracting job fields from description...")
        job_fields = {}

        self._protected_extractor(description, job_fields)

        print("All threads finished.")
        print("Job fields extracted successfully:\n")
        print(job_fields)

        return job_fields

    def fix_job_fields(self, job_fields):
        print("Fixing job fields...")

        job_fields_fixed = job_fields.copy()

        try:
            self.processor.fix_schedule_fields(job_fields_fixed)
            self.processor.fix_type_of_applicant_fields(job_fields_fixed)
            self.processor.fix_work_mode_fields(job_fields_fixed)
            return job_fields_fixed

        except Exception as e:
            print(f"An error occurred while fixing job fields: {e}")
            return job_fields

    def validate_fields(self, job_fields):
        try:
            print("Validating job fields...")

            if not job_fields:
                print("No job fields to validate.")
                return None

            job_fields_validated = job_fields.copy()

            self._protected_validator(job_fields_validated)

            print("All threads finished.")
            print("Job fields validated successfully:\n")
            print(job_fields_validated)

            return job_fields_validated
        except Exception as e:
            print(f"An error occurred while validating job fields: {e}")
            return job_fields

    def _protected_extractor(self, description, job_fields):
        with self.lock:
            start_forms_threads_extract(description, job_fields)

    def _protected_validator(self, job_fields_validated):
        with self.lock:
            start_forms_threads_validate(job_fields_validated)