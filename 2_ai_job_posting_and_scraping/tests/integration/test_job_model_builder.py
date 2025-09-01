import unittest
from src.job_model_builder import JobModelBuilder
from src.job_modeler import JobModelFromBot, JobModelFromScraper
from src.uni_bot.steps_config import forms


class TestJobModelBuilderIntegration(unittest.TestCase):
    def setUp(self):
        self.builder = JobModelBuilder()

    def build_full_form_data(self):
        return {
            'company': 'Unilinkr',
            'degree_of_specialization': 'Non-specialized',
            'job_title': 'Engenheiro de Software',
            'work_area': 'Catering',
            'job_description': 'Desenvolvimento de software.',
            'work_mode': 'Remote',
            'job_address': 'Rua Exemplo, 123',
            'job_country': 'Portugal',
            'district': 'Lisboa',
            'job_city': 'Lisboa',
            'lat': '38.7223',
            'lng': '-9.1393',
            'pin_code': '1000-000',
            'geo_radius': '50',
            'schedule_type': 'Full-Time',
            'start_date_full_time': '2024-09-01',
            'end_date_full_time': '2025-09-01',
            'vacancies_full_time': '2',
            'shifts': '1',
            'shift_name': '',
            'start_date_shift': '',
            'end_date_shift': '',
            'vacancies_shift': '',
            'custom_shift_name': '',
            'start_date_custom': '',
            'end_date_custom': '',
            'vacancies_custom': '',
            'payment_frequency': 'Monthly',
            'amount': '2000',
            'how_to_pay_student': 'Green Receipts',
            'type_of_applicant': 'Public',
            'teams_amount': '1',
            'team_Ids': '1',
            'benefits': 'Seguro de saúde, Cartão refeição',
        }

    def test_build_from_bot_with_full_form(self):
        job_fields = self.build_full_form_data()
        result = self.builder.build_from_bot(job_fields)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, JobModelFromBot)
        self.assertEqual(getattr(result, 'job_title', None), job_fields['job_title'])
        self.assertEqual(getattr(result, 'job_address', None), job_fields['job_address'] + ', ' + job_fields['district'] + ', ' + job_fields['job_country'])
        self.assertEqual(getattr(result, 'job_description', None), job_fields['job_description'])

    def test_build_from_scraper_with_full_form(self):
        scraped_data = self.build_full_form_data()
        result = self.builder.build_from_scraper(scraped_data)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, JobModelFromScraper)
        self.assertEqual(getattr(result, 'job_title', None), scraped_data['job_title'])
        self.assertEqual(getattr(result, 'job_address', None), scraped_data['job_address'])
        self.assertEqual(getattr(result, 'job_description', None), scraped_data['job_description'])

    def test_build_from_bot_with_invalid_data(self):
        invalid_data = {k: None for k in self.build_full_form_data().keys()}
        result = self.builder.build_from_bot(invalid_data)
        self.assertIsNone(result)

    def test_build_from_scraper_with_invalid_data(self):
        invalid_data = {k: None for k in self.build_full_form_data().keys()}
        result = self.builder.build_from_scraper(invalid_data)
        self.assertIsInstance(result, JobModelFromScraper)
        
    def test_build_from_bot_with_empty_fields(self):
        empty_data = {k: '' for k in self.build_full_form_data().keys()}
        result = self.builder.build_from_bot(empty_data)
        self.assertIsInstance(result, JobModelFromBot)

    def test_build_from_scraper_with_empty_fields(self):
        empty_data = {k: '' for k in self.build_full_form_data().keys()}
        result = self.builder.build_from_scraper(empty_data)
        self.assertIsInstance(result, JobModelFromScraper)    

if __name__ == "__main__":
    unittest.main()
