import unittest
from unittest.mock import patch, MagicMock
from src.uni_scraper.scraper_processor import ScraperProcessor

class TestScraperProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ScraperProcessor()

    @patch('src.uni_scraper.scraper_processor.ScraperNetEmpregos')
    def test_scrape_net_empregos(self, MockScraperNetEmpregos):
        mock_instance = MockScraperNetEmpregos.return_value
        mock_instance.scrape.return_value = [{'job_fields': {'job_title': 'Dev'}, 'source_link': 'link1'}]
        result = self.processor.scrape('net-empregos', 'https://www.net-empregos.com')
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1) # type: ignore
        self.assertEqual(result[0]['job_fields']['job_title'], 'Dev') # type: ignore
        self.assertEqual(result[0]['source_link'], 'link1') # type: ignore
        mock_instance.scrape.assert_called_once()
        MockScraperNetEmpregos.assert_called_once_with('https://www.net-empregos.com')

    def test_scrape_unknown_site(self):
        with patch('builtins.print') as mock_print:
            result = self.processor.scrape('unknown-site', 'https://dummy.url')
            self.assertIsNone(result)
            mock_print.assert_any_call('Site unknown-site não implementado.')

if __name__ == '__main__':
    unittest.main()
