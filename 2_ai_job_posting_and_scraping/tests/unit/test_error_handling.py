import unittest
from unittest.mock import patch
import threading

from src.interactor.bot_controller import BotController
from src.interactor.flow_controller import FlowController
from src.interactor.scraper_controller import ScraperController


class TestErrorHandling(unittest.TestCase):
    
    def setUp(self):
        self.bot_controller = BotController()
        self.flow_controller = FlowController()
        self.scraper_controller = ScraperController()

    def test_bot_controller_extract_job_exception(self):
        with patch.object(self.bot_controller.flow_controller, 'run_flow') as mock_run:
            mock_run.side_effect = ValueError("Invalid job description format")
            result = self.bot_controller.extract_job("corrupted input")
            self.assertIsNone(result)

    def test_bot_controller_scrape_jobs_exception(self):
        with patch.object(self.bot_controller.scraper_controller, 'scraper') as mock_scraper:
            mock_scraper.side_effect = ConnectionError("Network unavailable")
            result = self.bot_controller.scrape_jobs()
            self.assertIsNone(result)

    def test_flow_controller_threading_exception(self):
        with patch('src.interactor.flow_controller.start_forms_threads_extract') as mock_extract:
            mock_extract.side_effect = threading.ThreadError("Thread creation failed")
            result = self.flow_controller.extract_job_fields("test description")
            self.assertIsInstance(result, dict)

    def test_flow_controller_validation_exception(self):
        test_fields = {"job_title": "Developer", "invalid_field": None}
        with patch('src.interactor.flow_controller.start_forms_threads_validate') as mock_validate:
            mock_validate.side_effect = KeyError("Required field missing")
            result = self.flow_controller.validate_fields(test_fields)
            self.assertEqual(result, test_fields)

    def test_flow_controller_none_description(self):
        result = self.flow_controller.extract_job_fields(None)
        self.assertIsInstance(result, dict)

    def test_flow_controller_empty_job_fields(self):
        result = self.flow_controller.validate_fields({})
        self.assertIsNone(result)

    def test_flow_controller_none_job_fields(self):
        result = self.flow_controller.validate_fields(None)
        self.assertIsNone(result)

    def test_job_model_builder_exception(self):
        test_fields = {"invalid": "data"}
        with patch.object(self.flow_controller.builder, 'build_from_bot') as mock_build:
            mock_build.side_effect = AttributeError("Missing required attribute")
            result = self.flow_controller.run_flow(job_fields=test_fields, create_nlp_model=True)
            self.assertIsNone(result)

    def test_scraper_controller_website_failure(self):
        with patch('src.uni_scraper.scraper_processor.ScraperProcessor.scrape') as mock_scrape:
            mock_scrape.side_effect = [
                None,  # First website fails
                [{"job_fields": {"title": "Developer"}}],  # Second succeeds
                TimeoutError("Timeout"),  # Third times out
            ]
            with patch('src.uni_scraper.websites.websites', {"site1": "url1", "site2": "url2", "site3": "url3"}):
                result = self.scraper_controller.scraper()
                self.assertIsInstance(result, list)

    def test_memory_pressure_handling(self):
        large_description = "x" * (10 * 1024 * 1024)  # 10MB string
        with patch.object(self.flow_controller, 'extract_job_fields') as mock_extract:
            mock_extract.side_effect = MemoryError("Not enough memory")
            result = self.bot_controller.extract_job(large_description)
            self.assertIsNone(result)

    def test_concurrent_access_threading_lock(self):
        results = []
        exceptions = []
        def extract_worker(description):
            try:
                result = self.flow_controller.extract_job_fields(f"Job {description}")
                results.append(result)
            except Exception as e:
                exceptions.append(e)
        threads = []
        for i in range(5):
            thread = threading.Thread(target=extract_worker, args=(i,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        self.assertEqual(len(exceptions), 0)
        self.assertEqual(len(results), 5)

    def test_data_processor_fix_methods_exception(self):
        with patch.object(self.flow_controller.processor, 'fix_schedule_fields') as mock_fix:
            mock_fix.side_effect = ValueError("Invalid schedule format")
            test_fields = {"schedule": "invalid"}
            result = self.flow_controller.fix_job_fields(test_fields)
            self.assertEqual(result, test_fields)

    def test_network_timeout_handling(self):
        with patch('src.uni_scraper.scraper_processor.ScraperProcessor.scrape') as mock_scrape:
            mock_scrape.side_effect = [
                TimeoutError("Connection timeout"),
                ConnectionError("Network unreachable"),
                None  # No data returned
            ]
            with patch('src.uni_scraper.websites.websites', {"site1": "url1", "site2": "url2", "site3": "url3"}):
                result = self.scraper_controller.scraper()
                self.assertIsInstance(result, list)

    def test_various_exception_types(self):
        exception_types = [
            ValueError,
            TypeError,
            AttributeError,
            KeyError,
            IndexError,
            RuntimeError
        ]
        for exception_type in exception_types:
            with patch.object(self.bot_controller.flow_controller, 'run_flow') as mock_run:
                mock_run.side_effect = exception_type("Test exception")
                result = self.bot_controller.extract_job("test")
                self.assertIsNone(result)

    def test_partial_data_corruption(self):
        corrupted_fields = {
            "job_title": "Developer",
            "corrupted_field": None,
            "skills": ["Python", None, "JavaScript"],
            "salary": {"min": "invalid", "max": 5000}
        }
        result = self.flow_controller.validate_fields(corrupted_fields)
        self.assertIsInstance(result, dict)

    def test_rate_limiting_simulation(self):
        call_count = {"count": 0}
        def rate_limited_scrape(*args, **kwargs):
            call_count["count"] += 1
            if call_count["count"] <= 3:
                raise ConnectionError("Rate limited - 429 Too Many Requests")
            return [{"job_fields": {"title": "Developer"}}]
        with patch('src.uni_scraper.scraper_processor.ScraperProcessor.scrape', side_effect=rate_limited_scrape):
            with patch('src.uni_scraper.websites.websites', {"site1": "url1"}):
                result = self.scraper_controller.scraper()
                self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()
