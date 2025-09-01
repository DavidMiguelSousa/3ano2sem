import unittest
from unittest.mock import patch, MagicMock
from src.interactor.flow_controller import FlowController
from src.uni_bot.steps_config import forms

class TestFlowController(unittest.TestCase):
    def setUp(self):
        self.controller = FlowController()
        self.example_job_fields = {
            'company': 'Company David',
            'degree_of_specialization': 'Specialized',
            'job_title': 'Backend Developer',
            'job_description': 'O trabalho visa construir APIs e manter bases de dados em tempo integral por um período de 4 meses',
            'work_area': 'Promotion & Brand Activation',
            'work_mode': 'remote',
            'job_address': 'Rua das Flores 100, Porto, Portugal',
            'job_country': 'Portugal',
            'district': 'Porto',
            'job_city': 'Porto',
            'lat': '',
            'lng': '',
            'pin_code': '',
            'geo_radius': '25',
            'payment_frequency': 'Monthly',
            'amount': '1400€',
            'how_to_pay_student': 'Green Receipts',
            'type_of_applicant': 'Public',
            'benefits': 'Acesso a seguro de saúde e eventos de team-building',
            'teams_amount': '2',
            'team_ids': '2',
            'schedule_type': 'Full-time',
            'start_date_full_time': '01/08/2025',
            'end_date_full_time': '31/10/2025',
            'vacancies_full_time': '2',
            'shifts': '',
            'shift_name': '',
            'start_date_shift': '',
            'end_date_shift': '',
            'vacancies_shift': '',
            'custom_shift_name': '',
            'start_date_custom': '',
            'end_date_custom': '',
            'vacancies_custom': ''
        }

    def test_flow_controller_extract_and_validate(self):
        with patch.object(self.controller, 'extract_job_fields') as mock_extract, \
             patch.object(self.controller, 'validate_fields') as mock_validate, \
             patch.object(self.controller.builder, 'build_from_bot') as mock_build_from_bot:
            mock_extract.return_value = self.example_job_fields.copy()
            mock_validate.return_value = self.example_job_fields.copy()
            mock_build_from_bot.return_value = {'job': 'model'}
            result = self.controller.run_flow(description='Company X', extract=True)
            self.assertEqual(result, {'job': 'model'})
            mock_extract.assert_called_once()
            mock_validate.assert_called_once()
            mock_build_from_bot.assert_called_once()

    def test_flow_controller_validate_only(self):
        with patch.object(self.controller, 'validate_fields') as mock_validate, \
             patch.object(self.controller.builder, 'build_from_bot') as mock_build_from_bot:
            mock_validate.return_value = self.example_job_fields.copy()
            mock_build_from_bot.return_value = {'job': 'model'}
            result = self.controller.run_flow(job_fields=self.example_job_fields.copy(), extract=True)
            self.assertEqual(result, {'job': 'model'})
            mock_validate.assert_called_once()
            mock_build_from_bot.assert_called_once()

    def test_flow_controller_create_nlp_model(self):
        with patch.object(self.controller.builder, 'build_from_bot') as mock_build_from_bot:
            mock_build_from_bot.return_value = {'job': 'model'}
            result = self.controller.run_flow(job_fields=self.example_job_fields.copy(), create_nlp_model=True)
            self.assertEqual(result, {'job': 'model'})
            mock_build_from_bot.assert_called_once()

    def test_flow_controller_create_scraper_model(self):
        with patch.object(self.controller.builder, 'build_from_scraper') as mock_build_from_scraper:
            mock_build_from_scraper.return_value = {'scraper': 'model'}
            result = self.controller.run_flow(job_fields=self.example_job_fields.copy(), create_scraper_model=True)
            self.assertEqual(result, {'scraper': 'model'})
            mock_build_from_scraper.assert_called_once()

    @patch('src.interactor.flow_controller.start_forms_threads_extract')
    def test_extract_job_fields(self, mock_extract):
        def fake_extract(desc, job_fields):
            job_fields.clear()
            job_fields['company'] = 'Company Y'
        mock_extract.side_effect = fake_extract
        result = self.controller.extract_job_fields('desc')
        self.assertEqual(result, {'company': 'Company Y'})

    def test_fix_job_fields(self):
        with patch.object(self.controller.processor, 'fix_schedule_fields') as mock_fix_schedule, \
             patch.object(self.controller.processor, 'fix_type_of_applicant_fields') as mock_fix_type, \
             patch.object(self.controller.processor, 'fix_work_mode_fields') as mock_fix_work_mode:
            mock_fix_schedule.side_effect = lambda x: x.update({'fixed': True})
            mock_fix_type.side_effect = lambda x: x
            mock_fix_work_mode.side_effect = lambda x: x
            job_fields = self.example_job_fields.copy()
            result = self.controller.fix_job_fields(job_fields)
            self.assertIn('fixed', result)

    @patch('src.interactor.flow_controller.start_forms_threads_validate')
    def test_validate_fields(self, mock_validate):
        def fake_validate(job_fields):
            job_fields['validated'] = True
        mock_validate.side_effect = fake_validate
        job_fields = {field: "dummy" for field in forms["fields"]}
        result = self.controller.validate_fields(job_fields)
        self.assertIsInstance(result, dict)
        self.assertIn('validated', result) # type: ignore
        for key in result.keys(): # type: ignore
            self.assertIn(key, forms["fields"] + ["validated"])

if __name__ == '__main__':
    unittest.main()
