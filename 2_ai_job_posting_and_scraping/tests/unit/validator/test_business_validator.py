import unittest
from src.validator.business_validator import BusinessValidator
from src.uni_bot.steps_config import forms
from src.uni_bot.options_config import options_list

class TestBusinessValidator(unittest.TestCase):
    def setUp(self):
        self.validator = BusinessValidator(forms_config=forms, options_provider=options_list)
        self.rules = forms["rules"]
        self.fields = forms["fields"]

    def build_valid_job_forms(self):
        valid = {}
        for field in self.fields:
            if field in ["start_date_full_time", "end_date_full_time"]:
                valid[field] = "06/06/2025"
            elif field in ["start_date_shift", "end_date_shift"]:
                valid[field] = "07/06/2025"
            elif field in ["start_date_custom", "end_date_custom"]:
                valid[field] = "08/06/2025"
            elif field == "pin_code":
                valid[field] = "1234-567"
            elif field == "amount":
                valid[field] = "1000"
            elif field in ["lat", "lng", "geo_radius", "vacancies_full_time", "shifts", "vacancies_shift", "vacancies_custom", "teams_amount"]:
                valid[field] = "1"
            elif field == "job_title":
                valid[field] = "Software Engineer"
            elif field == "job_description":
                valid[field] = "Descrição válida."
            elif field == "benefits":
                valid[field] = "Seguro de saúde, Cartão refeição"
            elif field in ["degree_of_specialization", "work_area", "work_mode", "schedule_type", "payment_frequency", "how_to_pay_student", "type_of_applicant"]:
                opts = options_list(field)
                valid[field] = opts[0] if opts else "SomeOption"
            else:
                valid[field] = "Valor válido"
        return valid

    def build_empty_job_forms(self):
        return {field: "" for field in self.fields}

    def build_invalid_job_forms(self):
        invalid = {}
        for field in self.fields:
            if field in ["start_date_full_time", "end_date_full_time", "start_date_shift", "end_date_shift", "start_date_custom", "end_date_custom"]:
                invalid[field] = "2025-06-05"
            elif field == "pin_code":
                invalid[field] = "ABC-XYZ"
            elif field == "amount":
                invalid[field] = "mil euros"
            elif field in ["lat", "lng", "geo_radius", "vacancies_full_time", "shifts", "vacancies_shift", "vacancies_custom", "teams_amount"]:
                invalid[field] = "mil"
            elif field in ["degree_of_specialization", "work_area", "work_mode", "schedule_type", "payment_frequency", "how_to_pay_student", "type_of_applicant"]:
                invalid[field] = "ValorInvalidoUnico"
            else:
                invalid[field] = ""
        return invalid

    def test_validate_fields_valid(self):
        form = self.build_valid_job_forms()
        for field_name, field_value in form.items():
            with self.subTest(field_name=field_name, field_value=field_value):
                is_valid = self.validator.validate(field_name, field_value)
                rule = next((r["value"] for r in self.rules if r["field"] == field_name), None)
                if rule == "options":
                    self.assertTrue(is_valid, f"Expected valid for options in {field_name}")
                elif rule == "postal_code":
                    self.assertTrue(is_valid, f"Expected valid postal code for {field_name}")
                elif rule == "numeric":
                    self.assertTrue(is_valid, f"Expected valid numeric value for {field_name}")
                elif rule == "date":
                    self.assertTrue(is_valid, f"Expected valid date for {field_name}")
                else:
                    self.assertTrue(is_valid, f"Expected valid text for {field_name}")

    def test_validate_fields_empty(self):
        form = self.build_empty_job_forms()
        for field_name, field_value in form.items():
            with self.subTest(field_name=field_name, field_value=field_value):
                is_valid = self.validator.validate(field_name, field_value)
                self.assertFalse(is_valid, f"Expected invalid for empty value in {field_name}")

    def test_validate_fields_invalid(self):
        form = self.build_invalid_job_forms()
        for field_name, field_value in form.items():
            with self.subTest(field_name=field_name, field_value=field_value):
                is_valid = self.validator.validate(field_name, field_value)
                self.assertFalse(is_valid, f"Expected invalid for clearly invalid value in {field_name}")

if __name__ == "__main__":
    unittest.main()
