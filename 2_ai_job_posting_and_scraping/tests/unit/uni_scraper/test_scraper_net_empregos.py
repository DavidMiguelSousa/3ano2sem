import unittest
from unittest.mock import patch, MagicMock
from src.uni_scraper.scraper_processor import ScraperNetEmpregos

class TestScraperNetEmpregos(unittest.TestCase):
    def setUp(self):
        self.base_url = 'https://www.net-empregos.com'
        self.cookies_path = '/tmp/fake_cookies.json'

    @patch('src.uni_scraper.scraper_processor.webdriver.Chrome')
    @patch('src.uni_scraper.scraper_processor.FlowController')
    def test_create_driver(self, MockFlowController, MockChrome):
        scraper = ScraperNetEmpregos(self.base_url, self.cookies_path)
        driver = scraper.create_driver()
        self.assertTrue(MockChrome.called)
        self.assertIsNotNone(driver)

    @patch('src.uni_scraper.scraper_processor.webdriver.Chrome')
    @patch('src.uni_scraper.scraper_processor.FlowController')
    def test_close_driver(self, MockFlowController, MockChrome):
        scraper = ScraperNetEmpregos(self.base_url, self.cookies_path)
        scraper.driver = MagicMock()
        scraper.close_driver()
        scraper.driver.quit.assert_called_once()

    @patch('src.uni_scraper.scraper_processor.os.path.exists', return_value=True)
    @patch('src.uni_scraper.scraper_processor.json.load', return_value=[{'name': 'cookie'}])
    @patch('src.uni_scraper.scraper_processor.open', create=True)
    @patch('src.uni_scraper.scraper_processor.webdriver.Chrome')
    @patch('src.uni_scraper.scraper_processor.FlowController')
    def test_load_cookies(self, MockFlowController, MockChrome, mock_open, mock_json_load, mock_exists):
        scraper = ScraperNetEmpregos(self.base_url, self.cookies_path)
        scraper.driver = MagicMock()
        scraper.load_cookies()
        scraper.driver.add_cookie.assert_called_with({'name': 'cookie'})

    @patch('src.uni_scraper.scraper_processor.ScraperNetEmpregos.safe_get')
    @patch('src.uni_scraper.scraper_processor.BeautifulSoup')
    @patch('src.uni_scraper.scraper_processor.FlowController')
    @patch('src.uni_scraper.scraper_processor.webdriver.Chrome')
    def test_parse_listing_page(self, MockChrome, MockFlowController, MockBeautifulSoup, mock_safe_get):
        scraper = ScraperNetEmpregos(self.base_url, self.cookies_path)
        mock_card = MagicMock()
        mock_a = MagicMock()
        mock_a.get.return_value = '/job/123'
        mock_card.find.return_value = mock_a
        MockBeautifulSoup.return_value.find_all.return_value = [mock_card]
        offers = scraper.parse_listing_page()
        self.assertEqual(offers, [{'link': f'{self.base_url}/job/123'}])

    @patch('src.uni_scraper.scraper_processor.ScraperNetEmpregos.safe_get')
    @patch('src.uni_scraper.scraper_processor.BeautifulSoup')
    @patch('src.uni_scraper.scraper_processor.FlowController')
    @patch('src.uni_scraper.scraper_processor.webdriver.Chrome')
    def test_parse_offer_page(self, MockChrome, MockFlowController, MockBeautifulSoup, mock_safe_get):
        mock_flow = MockFlowController.return_value
        mock_flow.extract_job_fields.return_value = {'job_title': 'Dev'}
        scraper = ScraperNetEmpregos(self.base_url, self.cookies_path)
        mock_title = MagicMock()
        mock_title.text.strip.return_value = 'Dev'
        mock_location = MagicMock()
        mock_location.text.strip.return_value = 'Lisboa'
        mock_desc = MagicMock()
        mock_desc.text.strip.return_value = 'Descrição'
        MockBeautifulSoup.return_value.find.side_effect = [mock_title, mock_location, mock_desc]
        result = scraper.parse_offer_page('https://www.net-empregos.com/job/123')
        self.assertEqual(result['job_fields'], {'job_title': 'Dev'})
        self.assertEqual(result['source_link'], 'https://www.net-empregos.com/job/123')

    @patch('src.uni_scraper.scraper_processor.ScraperNetEmpregos.parse_listing_page')
    @patch('src.uni_scraper.scraper_processor.ScraperNetEmpregos.parse_offer_page')
    @patch('src.uni_scraper.scraper_processor.webdriver.Chrome')
    @patch('src.uni_scraper.scraper_processor.FlowController')
    def test_scrape(self, MockFlowController, MockChrome, mock_parse_offer_page, mock_parse_listing_page):
        scraper = ScraperNetEmpregos(self.base_url, self.cookies_path)
        mock_parse_listing_page.return_value = [{'link': 'https://www.net-empregos.com/job/123'}]
        mock_parse_offer_page.return_value = {'job_fields': {'job_title': 'Dev'}, 'source_link': 'https://www.net-empregos.com/job/123'}
        result = scraper.scrape()
        self.assertEqual(result, [{'job_fields': {'job_title': 'Dev'}, 'source_link': 'https://www.net-empregos.com/job/123'}])
        mock_parse_offer_page.assert_called_once_with('https://www.net-empregos.com/job/123')

if __name__ == '__main__':
    unittest.main()
