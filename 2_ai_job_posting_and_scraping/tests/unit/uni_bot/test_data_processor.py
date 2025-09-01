import unittest
from unittest.mock import patch, MagicMock
from src.uni_bot.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    @patch('src.uni_bot.data_processor.ai_call')
    @patch('src.uni_bot.data_processor.ai_extractor')
    def test_extract_section(self, mock_extractor, mock_ai_call):
        mock_ai_call.return_value = {'company': 'Empresa X'}
        result = self.processor.extract_section('details', ['company'], 'desc')
        self.assertEqual(result, {'company': 'Empresa X'})
        mock_ai_call.assert_called_once()

    @patch('src.uni_bot.data_processor.ai_date_fixer')
    def test_date_fixer(self, mock_date_fixer):
        mock_date_fixer.return_value = '01/01/2025'
        result = self.processor.date_fixer('2025-01-01')
        self.assertEqual(result, '01/01/2025')
        mock_date_fixer.assert_called_once_with('2025-01-01')

    @patch('src.uni_bot.data_processor.DataProcessor.extract_section')
    def test_extract_section_fields_updates_job_fields(self, mock_extract_section):
        mock_extract_section.return_value = {'company': 'Empresa Y'}
        job_fields = {}
        self.processor.extract_section_fields('desc', ['company'], job_fields, 'details')
        self.assertEqual(job_fields['company'], 'Empresa Y')

    def test_normalize(self):
        self.assertEqual(self.processor.normalize(' Café-Doce. '), 'cafedoce')
        self.assertEqual(self.processor.normalize('Árvore'), 'arvore')
        self.assertEqual(self.processor.normalize(123), 123)

    @patch('src.uni_bot.data_processor.options_list')
    def test_fix_schedule_fields_valid(self, mock_options_list):
        mock_options_list.return_value = ['Full-Time', 'Part-Time', 'Custom']
        job_fields = {'schedule_type': 'Full-Time'}
        self.processor.fix_schedule_fields(job_fields)
        self.assertEqual(job_fields['schedule_type'], 'Full-Time')

    @patch('src.uni_bot.data_processor.options_list')
    def test_fix_schedule_fields_invalid(self, mock_options_list):
        mock_options_list.return_value = ['Full-Time', 'Part-Time', 'Custom']
        job_fields = {'schedule_type': 'Invalid'}
        self.processor.fix_schedule_fields(job_fields)
        self.assertEqual(job_fields['schedule_type'], '')

    @patch('src.uni_bot.data_processor.options_list')
    def test_fix_type_of_applicant_fields_valid(self, mock_options_list):
        mock_options_list.return_value = ['Public', 'Private']
        job_fields = {'type_of_applicant': 'Public'}
        self.processor.fix_type_of_applicant_fields(job_fields)
        self.assertEqual(job_fields['type_of_applicant'], 'Public')

    @patch('src.uni_bot.data_processor.options_list')
    def test_fix_type_of_applicant_fields_invalid(self, mock_options_list):
        mock_options_list.return_value = ['Public', 'Private']
        job_fields = {'type_of_applicant': 'Outro'}
        self.processor.fix_type_of_applicant_fields(job_fields)
        self.assertEqual(job_fields['type_of_applicant'], '')

    def test_fix_work_mode_fields(self):
        job_fields = {'work_mode': 'hybrid'}
        self.processor.fix_work_mode_fields(job_fields)
        self.assertEqual(job_fields['work_mode'], 'remote')
        job_fields = {'work_mode': 'remote'}
        self.processor.fix_work_mode_fields(job_fields)
        self.assertEqual(job_fields['work_mode'], 'remote')

if __name__ == '__main__':
    unittest.main()
