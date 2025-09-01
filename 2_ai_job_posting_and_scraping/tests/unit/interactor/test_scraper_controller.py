import unittest
from unittest.mock import patch, MagicMock
from src.interactor.scraper_controller import ScraperController

class TestScraperController(unittest.TestCase):
    def setUp(self):
        self.controller = ScraperController()
        self.controller.flow_controller = MagicMock()
        self.controller.scraper_processor = MagicMock()

    def test_scraper_success_single_job(self):
        self.controller.scraper_processor.scrape.return_value = [
            {'job_fields': {'job_title': 'Dev'}, 'source_link': 'link1'}
        ]
        self.controller.flow_controller.run_flow.return_value = {'job_title': 'Dev'}
        with patch('src.interactor.scraper_controller.JobModelFromScraper') as MockJobModel, \
             patch('src.interactor.scraper_controller.websites', {'onlysite': 'https://dummy.url'}):
            mock_job = MagicMock()
            mock_job.to_dict.return_value = {'job_title': 'Dev'}
            MockJobModel.return_value = mock_job
            result = self.controller.scraper()
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['job_fields']['job_title'], 'Dev')
            self.assertEqual(result[0]['source_link'], 'link1')
            self.assertIn(result[0]['information'], ['Completo', 'Incompleto'])

    def test_scraper_empty(self):
        self.controller.scraper_processor.scrape.return_value = []
        with patch('src.interactor.scraper_controller.websites', {'onlysite': 'https://dummy.url'}):
            result = self.controller.scraper()
            self.assertEqual(result, [])

    def test_scraper_none(self):
        self.controller.scraper_processor.scrape.return_value = None
        with patch('src.interactor.scraper_controller.websites', {'onlysite': 'https://dummy.url'}):
            result = self.controller.scraper()
            self.assertEqual(result, [])

    def test_scraper_multiple_jobs(self):
        self.controller.scraper_processor.scrape.return_value = [
            {'job_fields': {'job_title': 'Dev1'}, 'source_link': 'link1'},
            {'job_fields': {'job_title': 'Dev2'}, 'source_link': 'link2'}
        ]
        self.controller.flow_controller.run_flow.side_effect = lambda **kwargs: kwargs['job_fields']
        with patch('src.interactor.scraper_controller.JobModelFromScraper') as MockJobModel, \
             patch('src.interactor.scraper_controller.websites', {'onlysite': 'https://dummy.url'}):
            mock_job = MagicMock()
            mock_job.to_dict.side_effect = lambda: {'job_title': mock_job.job_title}
            MockJobModel.side_effect = lambda job_fields: MagicMock(to_dict=MagicMock(return_value=job_fields))
            result = self.controller.scraper()
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['job_fields']['job_title'], 'Dev1')
            self.assertEqual(result[1]['job_fields']['job_title'], 'Dev2')

    def test_normalize_job_fields_defaults(self):
        job_fields = {}
        normalized = self.controller.normalize_job_fields(job_fields)
        self.assertIn('company', normalized)
        self.assertIn('job_title', normalized)
        self.assertEqual(normalized['job_country'], 'Portugal')

    def test_information_incompleto(self):
        job_fields = {'job_title': ''}
        info = self.controller.information(job_fields)
        self.assertEqual(info, 'Incompleto')

    def test_information_completo(self):
        job_fields = {'job_title': 'Dev'}
        info = self.controller.information(job_fields)
        self.assertEqual(info, 'Completo')

if __name__ == '__main__':
    unittest.main()
