from src.ai_gateway.ai_gateway import ai_call, ai_extractor, ai_date_fixer
from src.uni_bot.options_config import options_list
from src.uni_bot.steps_config import forms

import unicodedata
from threading import Lock
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.lock = Lock()

    def extractor(self, description, section_steps, job_fields, section):
        try:
            self.extract_section_fields(description, section_steps, job_fields, section)
            return job_fields
        except Exception as e:
            print(f"An error occurred while extracting section fields: {e}")
            return None

    def extract_section_fields(self, description, section_steps, job_fields, section):
        today = datetime.today().strftime('%d/%m/%Y')
        full_description = f"Data: {today}\n{description}"
        ai_response = self.extract_section(section, section_steps, full_description)

        if ai_response:
            job_fields.update(ai_response)

    def extract_section(self, section, section_steps, description):
        return ai_call(
            ai_extractor,
            section=section,
            section_steps=section_steps,
            description=description
        )

    def date_fixer(self, date_str):
        return ai_date_fixer(date_str)

    def fix_schedule_fields(self, job_fields):
        section = "schedule_and_vacancies"
        schedule_options = [self.normalize(option) for option in options_list("scheduleType")]
        if "schedule_type" in job_fields:
            schedule_type = self.normalize(job_fields["schedule_type"])
            if schedule_type in schedule_options:
                for original_option in options_list("schedule_type"):
                    if self.normalize(original_option) == schedule_type:
                        print(f"Valid schedule type: {original_option}")
                        job_fields["schedule_type"] = original_option
                        break

                if schedule_type == "full-time":
                    self.clean_advanced_fields(job_fields, section, "part-time")
                    self.clean_advanced_fields(job_fields, section, "custom")
                elif schedule_type == "part-time":
                    self.clean_advanced_fields(job_fields, section, "full-time")
                    self.clean_advanced_fields(job_fields, section, "custom")
                elif schedule_type == "custom":
                    self.clean_advanced_fields(job_fields, section, "full-time")
                    self.clean_advanced_fields(job_fields, section, "part-time")
            else:
                job_fields["schedule_type"] = ""
                self._clear_all_schedule_types(job_fields, section)
        else:
            job_fields["schedule_type"] = ""
            self._clear_all_schedule_types(job_fields, section)

    def _clear_all_schedule_types(self, job_fields, section):
        for type_ in ["full-time", "part-time", "custom"]:
            self.clean_advanced_fields(job_fields, section, type_)

    def fix_type_of_applicant_fields(self, job_fields):
        section = "compensation_and_benefits"
        type_options = [self.normalize(option) for option in options_list("typeOfApplicant")]
        if "type_of_applicant" in job_fields:
            value = self.normalize(job_fields["type_of_applicant"])
            if value in type_options:
                for original_option in options_list("type_of_applicant"):
                    if self.normalize(original_option) == value:
                        print(f"Valid type of applicant: {original_option}")
                        job_fields["type_of_applicant"] = original_option
                        break
                if value == "public":
                    self.clean_advanced_fields(job_fields, section, "equipas")
            else:
                job_fields["type_of_applicant"] = ""
                self.clean_advanced_fields(job_fields, section, "equipas")
        else:
            job_fields["type_of_applicant"] = ""
            self.clean_advanced_fields(job_fields, section, "equipas")

    def clean_advanced_fields(self, job_fields, section, this_type):
        if section in forms["required_fields"] and "advanced" in forms["required_fields"][section]:
            advanced_fields = forms["required_fields"][section]["advanced"]
            if this_type in advanced_fields:
                for field in advanced_fields[this_type]:
                    if field in job_fields:
                        job_fields[field] = ""

    def fix_work_mode_fields(self, job_fields):
        if "work_mode" in job_fields and job_fields["work_mode"] == "hybrid":
            job_fields["work_mode"] = "remote"

    def normalize(self, value):
        if not isinstance(value, str):
            return value
        value = unicodedata.normalize("NFKD", value)
        value = value.encode("ascii", "ignore").decode("utf-8")
        return value.lower().strip().replace(",", "").replace(".", "").replace("-", "").replace(" ", "")
