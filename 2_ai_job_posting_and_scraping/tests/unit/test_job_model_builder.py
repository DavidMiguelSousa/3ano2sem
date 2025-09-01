import unittest

from src.job_model_builder import JobModelBuilder
from src.job_modeler import JobModelFromBot, JobModelFromScraper
from unittest.mock import patch, MagicMock

class TestJobModelBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = JobModelBuilder()

    def test_build_from_bot_success(self):
        mock_fields = {"titulo": "Dev", "empresa": "Unilinkr"}
        with patch('src.job_model_builder.JobModelFromBot') as mock_bot:
            mock_instance = MagicMock()
            mock_bot.return_value = mock_instance
            result = self.builder.build_from_bot(mock_fields)
            mock_bot.assert_called_once_with(mock_fields)
            self.assertEqual(result, mock_instance)

    def test_build_from_bot_failure(self):
        with patch('src.job_model_builder.JobModelFromBot', side_effect=Exception("Erro")) as mock_bot:
            result = self.builder.build_from_bot({"invalid": "data"})
            mock_bot.assert_called_once()
            self.assertIsNone(result)

    def test_build_from_scraper_success(self):
        mock_data = {"titulo": "Data Scientist", "localizacao": "Porto"}
        with patch('src.job_model_builder.JobModelFromScraper') as mock_scraper:
            mock_instance = MagicMock()
            mock_scraper.return_value = mock_instance
            result = self.builder.build_from_scraper(mock_data)
            mock_scraper.assert_called_once_with(mock_data)
            self.assertEqual(result, mock_instance)

    def test_build_from_scraper_failure(self):
        with patch('src.job_model_builder.JobModelFromScraper', side_effect=Exception("Erro scraper")) as mock_scraper:
            result = self.builder.build_from_scraper({"invalid": "data"})
            mock_scraper.assert_called_once()
            self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()