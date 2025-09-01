import unittest
from src.validator.field_processor import FieldProcessor
from src.uni_bot.options_config import options_list
from src.uni_bot.steps_config import forms

class TestFieldProcessorIntegrationReal(unittest.TestCase):
    def setUp(self):
        self.processor = FieldProcessor(forms_config=forms, options_list=options_list)

    def test_full_validation_details(self):
        job_fields = {
            "company": "Empresa Z",
            "degree_of_specialization": "Non-specialized",
            "job_title": "Engenheiro",
            "work_area": "Catering",
            "job_description": "Descrição qualquer.",
        }
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertEqual(result["company"], "Empresa Z")
        self.assertEqual(result["degree_of_specialization"], "Non-specialized")
        self.assertEqual(result["job_title"], "Engenheiro")
        self.assertEqual(result["work_area"], "Catering")
        self.assertEqual(result["job_description"], "Descrição qualquer")
        
    def test_full_validation_location(self):
        job_fields = {
            "job_address": "Rua Exemplo, 123",
            "job_country": "Portugal",
            "district": "Lisboa",
            "job_city": "Lisboa",
            "lat": "38.7223",
            "lng": "-9.1393",
            "pin_code": "1000-000",
            "geo_radius": "50",
            "work_mode": "Remote"
        }
        result = self.processor.validate_fields(job_fields, section="location")
        self.assertEqual(result["job_address"], "Rua Exemplo, 123")
        self.assertEqual(result["job_country"], "Portugal")
        self.assertEqual(result["district"], "Lisboa")
        self.assertEqual(result["job_city"], "Lisboa")
        self.assertEqual(result["lat"], "38.7223")
        self.assertEqual(result["lng"], "-9.1393")
        self.assertEqual(result["pin_code"], "1000-000")
        self.assertEqual(result["geo_radius"], "50")
        self.assertEqual(result["work_mode"], "Remote")
        
    def test_full_validation_schedule_and_vacancies(self):
        job_fields = {
            "schedule_type": "Full-Time",
            "start_date_full_time": "2024-09-01",
            "end_date_full_time": "2025-09-01",
            "vacancies_full_time": "2",
            "shifts": "1",
            "shift_name": "",
            "start_date_shift": "",
            "end_date_shift": "",
            "vacancies_shift": "",
            "custom_shift_name": "",
            "start_date_custom": "",
            "end_date_custom": "",
            "vacancies_custom": ""
        }
        result = self.processor.validate_fields(job_fields, section="schedule_and_vacancies")
        self.assertEqual(result["schedule_type"], "Full-Time")
        self.assertEqual(result["start_date_full_time"], "01/09/2024")
        self.assertEqual(result["end_date_full_time"], "01/09/2025")
        self.assertEqual(result["vacancies_full_time"], "2")
        self.assertEqual(result["shifts"], "1")
        
    def test_full_validation_payment_and_benefits(self):
        job_fields = {
            "payment_frequency": "Monthly",
            "amount": "2000",
            "how_to_pay_student": "Green Receipts",
            "type_of_applicant": "Public",
            "teams_amount": "1",
            "team_ids": "1",
            "benefits": "Seguro de saúde, Cartão refeição"
        }
        result = self.processor.validate_fields(job_fields, section="compensation_and_benefits")
        self.assertEqual(result["payment_frequency"], "Monthly")
        self.assertEqual(result["amount"], "2000")
        self.assertEqual(result["how_to_pay_student"], "Green Receipts")
        self.assertEqual(result["type_of_applicant"], "Public")
        self.assertEqual(result["teams_amount"], "1")
        self.assertEqual(result["team_ids"], "1")
        self.assertEqual(result["benefits"], "Seguro de saúde, Cartão refeição")

    def test_invalid_option_cleaned(self):
        job_fields = {"degree_of_specialization": "talvez"}
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertEqual(result["degree_of_specialization"], "")

    def test_extra_field_ignored(self):
        job_fields = {"company": "Empresa X", "campo_inexistente": "valor"}
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertIn("company", result)
        self.assertNotIn("campo_inexistente", result)

    def test_numeric_field(self):
        job_fields = {"lat": "41.1", "lng": "-8.6"}
        result = self.processor.validate_fields(job_fields, section="location")
        self.assertEqual(result["lat"], "41.1")
        self.assertEqual(result["lng"], "-8.6")

    def test_options_field(self):
        job_fields = {"work_mode": "On-site"}
        result = self.processor.validate_fields(job_fields, section="location")
        self.assertEqual(result["work_mode"], "On-site")

    def test_invalid_numeric(self):
        job_fields = {"lat": "abc"}
        result = self.processor.validate_fields(job_fields, section="location")
        self.assertEqual(result["lat"], "")

    def test_date_fallback(self):
        job_fields = {"start_date_full_time": "2026/01/31"}
        result = self.processor.validate_fields(job_fields, section="schedule_and_vacancies")
        self.assertIsInstance(result["start_date_full_time"], str)

if __name__ == '__main__':
    unittest.main()
