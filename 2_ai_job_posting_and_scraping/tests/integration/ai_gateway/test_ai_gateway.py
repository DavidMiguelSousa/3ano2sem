import unittest
from unittest.mock import patch
from src.ai_gateway import ai_gateway

class TestAIGatewayIntegration(unittest.TestCase):
    @patch('src.ai_gateway.ai_gateway.chat')
    def test_response_integration(self, mock_chat):
        mock_chat.return_value = {
            'message': {'content': '{"campo1": "valor1", "campo2": "valor2"}'}
        }
        prompt = "Extrai campos de teste"
        result = ai_gateway.response(prompt)
        self.assertEqual(result, '{"campo1": "valor1", "campo2": "valor2"}')

    @patch('src.ai_gateway.ai_gateway.response')
    def test_ai_extractor_integration(self, mock_response):
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

    def test_flatten_steps_integration(self):
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

    def test_flatten_steps_real(self):
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

    def test_ai_extractor_real(self):
        section = "compensation"
        section_steps = [
            {"question": "Qual é o salário?", "style": "number", "field": "amount"},
            {"question": "Qual é a frequência de pagamento?", "style": "options", "field": "payment_frequency"}
        ]
        description = "Oferta: Engenheiro de Software. Salário: 2000€. Pagamento mensal."
        result = ai_gateway.ai_extractor(section, section_steps, description)
        self.assertIsInstance(result, dict)
        self.assertIn("amount", result)
        self.assertIn("payment_frequency", result)

if __name__ == "__main__":
    unittest.main()