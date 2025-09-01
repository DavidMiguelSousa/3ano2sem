import unittest
from unittest.mock import patch, MagicMock
from src.ai_gateway import ai_gateway

class TestAIGateway(unittest.TestCase):
    @patch('src.ai_gateway.ai_gateway.chat')
    def test_response(self, mock_chat):
        mock_chat.return_value = {
            'message': {'content': 'Resposta simulada'}
        }
        prompt = "Teste de prompt"
        result = ai_gateway.response(prompt)
        self.assertEqual(result, 'Resposta simulada')

    @patch('src.ai_gateway.ai_gateway.response')
    def test_ai_date_fixer(self, mock_response):
        mock_response.return_value = '16/06/2026'
        value = '16 de junho de 2026'
        result = ai_gateway.ai_date_fixer(value)
        self.assertEqual(result, '16/06/2026')

    def test_flatten_steps(self):
        steps = [
            {"question": "Q1", "style": "S1", "field": "F1"},
            {"subfields": [
                {"question": "Q2", "style": "S2", "field": "F2"}
            ]}
        ]
        flat = ai_gateway.flatten_steps(steps)
        self.assertEqual(len(flat), 2)
        self.assertEqual(flat[0]["field"], "F1")
        self.assertEqual(flat[1]["field"], "F2")

    @patch('src.ai_gateway.ai_gateway.response')
    def test_ai_extractor(self, mock_response):
        mock_response.return_value = '{"campo1": "valor1", "campo2": "valor2"}'
        section = "secao"
        section_steps = [
            {"question": "Q1", "style": "S1", "field": "campo1"},
            {"question": "Q2", "style": "S2", "field": "campo2"}
        ]
        description = "Descrição de teste."
        result = ai_gateway.ai_extractor(section, section_steps, description)
        self.assertIsInstance(result, dict)
        self.assertIn("campo1", result)
        self.assertIn("campo2", result)

if __name__ == "__main__":
    unittest.main()
