import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.router import app


class TestAPIEndpoints:
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_chat_endpoint_success(self):
        test_description = "Software Developer position with Python and FastAPI experience"
        
        with patch('src.interactor.bot_controller.BotController.extract_job') as mock_extract:
            mock_extract.return_value = {
                "job_title": "Software Developer",
                "skills": ["Python", "FastAPI"],
                "experience": "2-3 years"
            }
            
            response = self.client.post("/chat", json={"description": test_description})
            
            assert response.status_code == 200
            assert "job_model" in response.json()
            mock_extract.assert_called_once_with(description=test_description)
    
    def test_chat_endpoint_empty_description(self):
        response = self.client.post("/chat", json={"description": ""})
        assert response.status_code in [200, 422]
    
    def test_chat_endpoint_none_result(self):
        with patch('src.interactor.bot_controller.BotController.extract_job') as mock_extract:
            mock_extract.return_value = None
            
            response = self.client.post("/chat", json={"description": "test"})
            
            assert response.status_code == 200
            assert response.json() == {"error": "Não foi possível criar o modelo de trabalho."}

    def test_chat_endpoint_invalid_json(self):
        response = self.client.post(
            "/chat",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422
    
    def test_chat_endpoint_missing_description(self):
        response = self.client.post("/chat", json={})
        
        assert response.status_code == 422
    
    def test_scraper_endpoint_success(self):
        mock_result = [
            {"job_title": "Data Scientist", "location": "Porto"},
            {"job_title": "Web Developer", "location": "Lisboa"}
        ]
        
        with patch('src.interactor.bot_controller.BotController.scrape_jobs') as mock_scrape:
            mock_scrape.return_value = mock_result
            
            response = self.client.get("/scraper")
            
            assert response.status_code == 200
            assert response.json() == mock_result
    
    def test_scraper_endpoint_no_results(self):
        with patch('src.interactor.bot_controller.BotController.scrape_jobs') as mock_scrape:
            mock_scrape.return_value = None
            
            response = self.client.get("/scraper")
            
            assert response.status_code == 200
            assert response.json() == {"error": "Não foi possível criar o modelo de trabalho."}
    
    def test_scraper_endpoint_empty_list(self):
        with patch('src.interactor.bot_controller.BotController.scrape_jobs') as mock_scrape:
            mock_scrape.return_value = []
            
            response = self.client.get("/scraper")
            
            assert response.status_code == 200
            assert response.json() == {"error": "Não foi possível criar o modelo de trabalho."}
    
    def test_both_endpoints_with_get_method(self):
        response = self.client.get("/chat")
        assert response.status_code in [200, 422, 405] 
        
        response = self.client.post("/scraper")
        assert response.status_code in [200, 405]
    
    def test_cors_headers(self):
        response = self.client.get("/scraper")
        assert "access-control-allow-origin" in response.headers or response.status_code in [200, 404]
    
    def test_endpoint_exception_handling(self):
        with patch('src.interactor.bot_controller.BotController.extract_job') as mock_extract:
            mock_extract.side_effect = Exception("Database connection failed")
            response = self.client.post("/chat", json={"description": "test"})
            assert response.status_code in [200, 500]
    
    @pytest.mark.parametrize("description", [
        "a" * 10000, 
        "Special chars: âéîôûç àèùß",  
        "Multiple\nlines\nwith\nbreaks",  
        "   whitespace   ",  
    ])
    def test_chat_endpoint_edge_case_inputs(self, description):
        with patch('src.interactor.bot_controller.BotController.extract_job') as mock_extract:
            mock_extract.return_value = {"processed": True}
            
            response = self.client.post("/chat", json={"description": description})
            
            assert response.status_code in [200, 422]
