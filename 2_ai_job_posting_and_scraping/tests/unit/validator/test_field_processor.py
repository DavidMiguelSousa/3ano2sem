import unittest
from unittest.mock import patch
from src.validator.field_processor import FieldProcessor

def fake_options_list(field):
    if field == "degree_of_specialization":
        return ["Specialized", "Non-specialized"]
    return []

class TestFieldProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = FieldProcessor(forms_config=None, options_list=fake_options_list)
        def validate(field_name, field_value):
            if field_value in ["", "inválido", "não sei"]:
                return False
            if field_name == "degree_of_specialization":
                return field_value in ["Specialized", "Non-specialized"]
            if field_name == "start_date_full_time":
                return field_value == "31/01/2026"
            return True
        self.processor.business_validator.validate = validate

    def test_valida_texto_valido(self):
        job_fields = {"company": "Empresa X"}
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertEqual(result["company"], "Empresa X")

    def test_valida_texto_invalido(self):
        job_fields = {"company": ""}
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertEqual(result["company"], "")

    def test_valida_opcao_valida(self):
        job_fields = {"degree_of_specialization": "Specialized"}
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertEqual(result["degree_of_specialization"], "Specialized")
    
    def test_valida_opcao_invalida(self):
        job_fields = {"degree_of_specialization": "talvez"}
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertEqual(result["degree_of_specialization"], "")

    def test_valida_data_fallback(self):
        # Mock the data_processor.date_fixer method specifically for this test
        original_date_fixer = self.processor.data_processor.date_fixer
        self.processor.data_processor.date_fixer = lambda date_str: "31/01/2026"
        
        job_fields = {"start_date_full_time": "2026/01/31"}
        result = self.processor.validate_fields(job_fields, section="schedule_and_vacancies")
        self.assertEqual(result["start_date_full_time"], "31/01/2026")
        
        # Restore original method
        self.processor.data_processor.date_fixer = original_date_fixer
        
    def test_valida_data_fallback_erro(self):
        job_fields = {"start_date_full_time": "inválido"}
        result = self.processor.validate_fields(job_fields, section="schedule_and_vacancies")
        self.assertEqual(result["start_date_full_time"], "")

    def test_ignora_campo_que_nao_esta_no_forms(self):
        job_fields = {"campo_inexistente": "valor"}
        result = self.processor.validate_fields(job_fields, section="details")
        self.assertNotIn("campo_inexistente", result)

    def test_cleaner_remove_não_sei(self):
        job_fields = {"company": "não sei", "degree_of_specialization": "não sei"}
        cleaned = self.processor._cleaner(job_fields, section="details")
        self.assertEqual(cleaned["company"], "")
        self.assertEqual(cleaned["degree_of_specialization"], "")

    def test_cleaner_opcao_invalida(self):
        job_fields = {"degree_of_specialization": "talvez"}
        cleaned = self.processor._cleaner(job_fields, section="details")
        self.assertEqual(cleaned["degree_of_specialization"], "")

    def test_cleaner_opcao_valida(self):
        job_fields = {"degree_of_specialization": "Non-specialized"}
        cleaned = self.processor._cleaner(job_fields, section="details")
        self.assertEqual(cleaned["degree_of_specialization"], "Non-specialized")

if __name__ == '__main__':
    unittest.main()
