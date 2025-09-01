import unittest
from unittest.mock import MagicMock
from src.interactor.bot_controller import BotController

class TestBotController(unittest.TestCase):
    def setUp(self):
        self.bot = BotController()
        self.bot.flow_controller = MagicMock()
        self.bot.scraper_controller = MagicMock()
        self.bot.scraper_controller.scraper = MagicMock()

    def test_extract_job_success(self):
        self.bot.flow_controller.run_flow.return_value = {'job_title': 'Developer'}
        result = self.bot.extract_job("Descrição: Título do trabalho é Developer")
        self.assertIsNotNone(result)
        self.assertEqual(result['job_title'], 'Developer') # type: ignore

    def test_extract_job_failure(self):
        self.bot.flow_controller.run_flow.side_effect = Exception("Erro")
        result = self.bot.extract_job("Descrição inválida")
        self.assertIsNone(result)

    def test_extract_job_empty(self):
        self.bot.flow_controller.run_flow.return_value = {}
        result = self.bot.extract_job("Descrição sem dados")
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_scrape_jobs_success(self):
        self.bot.scraper_controller.scraper.return_value = [{'job_fields': {}}]
        result = self.bot.scrape_jobs()
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 1) # type: ignore

    def test_scrape_jobs_failure(self):
        self.bot.scraper_controller.scraper.return_value = []
        result = self.bot.scrape_jobs()
        self.assertIsNone(result)

    def test_scrape_jobs_multiple(self):
        self.bot.scraper_controller.scraper.return_value = [
            {'job_fields': {'job_title': 'Dev1'}},
            {'job_fields': {'job_title': 'Dev2'}},
        ]
        result = self.bot.scrape_jobs()
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 2) # type: ignore
        self.assertIsInstance(result[0], dict) # type: ignore
        self.assertEqual(result[0]['job_fields']['job_title'], 'Dev1') # type: ignore
        self.assertEqual(result[1]['job_fields']['job_title'], 'Dev2') # type: ignore

    def test_scrape_jobs_none(self):
        self.bot.scraper_controller.scraper.return_value = None
        result = self.bot.scrape_jobs()
        self.assertIsNone(result)

    def test_run_flow_called_once(self):
        self.bot.extract_job("Descrição: Título do trabalho é Developer")
        self.bot.flow_controller.run_flow.assert_called_once()

if __name__ == '__main__':
    unittest.main()
