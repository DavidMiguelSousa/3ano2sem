import unittest
from src.uni_bot.data_processor import DataProcessor
from src.uni_bot.steps_config import forms

class TestDataProcessorIntegration(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
        self.default_job_fields = {
            'company': 'Company David',
            'degree_of_specialization': 'Specialized',
            'job_title': 'Backend Developer',
            'job_description': 'O trabalho visa construir APIs e manter bases de dados em tempo integral por um período de 4 meses',
            'work_area': 'Promotion & Brand Activation',
            'work_mode': 'remote',
            'job_address': 'Rua das Flores 100, Porto, Portugal',
            'job_country': 'Portugal',
            'district': 'Porto',
            'job_city': 'Porto',
            'lat': '',
            'lng': '',
            'pin_code': '',
            'geo_radius': '25',
            'payment_frequency': 'Monthly',
            'amount': '1400€',
            'how_to_pay_student': 'Green Receipts',
            'type_of_applicant': 'Public',
            'benefits': 'Acesso a seguro de saúde e eventos de team-building',
            'teams_amount': '2',
            'team_ids': '2',
            'schedule_type': 'Full-time',
            'start_date_full_time': '01/08/2025',
            'end_date_full_time': '31/10/2025',
            'vacancies_full_time': '2',
            'shifts': '',
            'shift_name': '',
            'start_date_shift': '',
            'end_date_shift': '',
            'vacancies_shift': '',
            'custom_shift_name': '',
            'start_date_custom': '',
            'end_date_custom': '',
            'vacancies_custom': ''
        }

    # def test_extract_and_validate_section_fields(self):
    #     job_fields = {}
    #     description = (
    #         "Empresa: Company David. "
    #         "Especialização: Specialized. "
    #         "Cargo: Backend Developer. "
    #         "Descrição: O trabalho visa construir APIs e manter bases de dados em tempo integral por um período de 4 meses. "
    #         "Área: Promotion & Brand Activation. "
    #         "Modo: remote. "
    #         "Endereço: Rua das Flores 100, Porto, Portugal. "
    #         "País: Portugal. "
    #         "Distrito: Porto. "
    #         "Cidade: Porto. "
    #         "Raio: 25. "
    #         "Pagamento: Monthly. "
    #         "Valor: 1400€. "
    #         "Pagamento estudante: Green Receipts. "
    #         "Tipo de candidato: Public. "
    #         "Benefícios: Acesso a seguro de saúde e eventos de team-building. "
    #         "Nº equipas: 2. "
    #         "ID equipa: 2. "
    #         "Tipo horário: Full-time. "
    #         "Início: 01/08/2025. "
    #         "Fim: 31/10/2025. "
    #         "Vagas: 2."
    #     )
    #     section = "details"
    #     section_steps = forms["steps"][section]
    #     result = self.processor.extractor(description, section_steps, job_fields, section)
    #     self.assertIsInstance(result, dict)
    #     # Só valida os campos realmente definidos no steps_config para a secção 'details'
    #     for field in [
    #         'company', 'degree_of_specialization', 'job_title', 'job_description', 'work_area'
    #     ]:
    #         self.assertIn(field, job_fields)
    #     # Campos que não pertencem à secção 'details' não devem estar presentes
    #     for field in [
    #         'work_mode', 'job_address', 'job_country', 'district', 'job_city', 'geo_radius',
    #         'payment_frequency', 'amount', 'how_to_pay_student', 'type_of_applicant', 'benefits',
    #         'teams_amount', 'team_ids', 'schedule_type', 'start_date_full_time', 'end_date_full_time', 'vacancies_full_time',
    #         'lat', 'lng', 'pin_code', 'shifts', 'shift_name', 'start_date_shift', 'end_date_shift', 'vacancies_shift',
    #         'custom_shift_name', 'start_date_custom', 'end_date_custom', 'vacancies_custom'
    #     ]:
    #         self.assertNotIn(field, job_fields)

    def test_extract_and_validate_details_section(self):
        job_fields = {}
        description = (
            "Empresa: Company David. "
            "Especialização: Specialized. "
            "Cargo: Backend Developer. "
            "Descrição: O trabalho visa construir APIs e manter bases de dados em tempo integral por um período de 4 meses. "
            "Área: Promotion & Brand Activation. "
        )
        section = "details"
        section_steps = forms["steps"][section]
        result = self.processor.extractor(description, section_steps, job_fields, section)
        self.assertIsInstance(result, dict)
        for field in ['company', 'degree_of_specialization', 'job_title', 'job_description', 'work_area']:
            self.assertIn(field, job_fields)
        for field in set(self.default_job_fields.keys()) - set(['company', 'degree_of_specialization', 'job_title', 'job_description', 'work_area']):
            self.assertNotIn(field, job_fields)

    def test_extract_and_validate_location_section(self):
        job_fields = {}
        description = (
            "Modo: remote. "
            "Endereço: Rua das Flores 100, Porto, Portugal. "
            "País: Portugal. "
            "Distrito: Porto. "
            "Cidade: Porto. "
            "Latitude: 41.1. "
            "Longitude: -8.6. "
            "Código postal: 1000-000. "
            "Raio: 25. "
        )
        section = "location"
        section_steps = forms["steps"][section]
        result = self.processor.extractor(description, section_steps, job_fields, section)
        self.assertIsInstance(result, dict)
        for field in ['work_mode', 'job_address', 'job_country', 'district', 'job_city', 'lat', 'lng', 'pin_code', 'geo_radius']:
            self.assertIn(field, job_fields)
        for field in set(self.default_job_fields.keys()) - set(['work_mode', 'job_address', 'job_country', 'district', 'job_city', 'lat', 'lng', 'pin_code', 'geo_radius']):
            self.assertNotIn(field, job_fields)

    def test_extract_and_validate_schedule_and_vacancies_section(self):
        job_fields = {}
        description = (
            "Tipo horário: Full-time. "
            "Início: 01/08/2025. "
            "Fim: 31/10/2025. "
            "Vagas: 2. "
            "Turnos: 1. "
        )
        section = "schedule_and_vacancies"
        section_steps = forms["steps"][section]
        result = self.processor.extractor(description, section_steps, job_fields, section)
        self.assertIsInstance(result, dict)
        for field in ['schedule_type', 'start_date_full_time', 'end_date_full_time', 'vacancies_full_time', 'shifts']:
            self.assertIn(field, job_fields)
        for field in set(self.default_job_fields.keys()) - set(['schedule_type', 'start_date_full_time', 'end_date_full_time', 'vacancies_full_time', 'shifts']):
            self.assertNotIn(field, job_fields)

    def test_extract_and_validate_compensation_and_benefits_section(self):
        job_fields = {}
        description = (
            "Pagamento: Monthly. "
            "Valor: 1400€. "
            "Pagamento estudante: Green Receipts. "
            "Tipo de candidato: Public. "
            "Benefícios: Acesso a seguro de saúde e eventos de team-building. "
            "Nº equipas: 2. "
            "ID equipa: 2. "
        )
        section = "compensation_and_benefits"
        section_steps = forms["steps"][section]
        result = self.processor.extractor(description, section_steps, job_fields, section)
        self.assertIsInstance(result, dict)
        for field in ['payment_frequency', 'amount', 'how_to_pay_student', 'type_of_applicant', 'benefits', 'teams_amount', 'team_ids']:
            self.assertIn(field, job_fields)
        for field in set(self.default_job_fields.keys()) - set(['payment_frequency', 'amount', 'how_to_pay_student', 'type_of_applicant', 'benefits', 'teams_amount', 'team_ids']):
            self.assertNotIn(field, job_fields)

    def test_fix_schedule_fields_integration(self):
        job_fields = self.default_job_fields.copy()
        self.processor.fix_schedule_fields(job_fields)
        self.assertEqual(job_fields["schedule_type"].lower(), "full-time")
        job_fields["schedule_type"] = "Invalid"
        self.processor.fix_schedule_fields(job_fields)
        self.assertEqual(job_fields["schedule_type"], "")

    def test_fix_type_of_applicant_fields_integration(self):
        job_fields = self.default_job_fields.copy()
        self.processor.fix_type_of_applicant_fields(job_fields)
        self.assertEqual(job_fields["type_of_applicant"], "Public")
        job_fields["type_of_applicant"] = "Outro"
        self.processor.fix_type_of_applicant_fields(job_fields)
        self.assertEqual(job_fields["type_of_applicant"], "")

    def test_fix_work_mode_fields_integration(self):
        job_fields = self.default_job_fields.copy()
        job_fields["work_mode"] = "hybrid"
        self.processor.fix_work_mode_fields(job_fields)
        self.assertEqual(job_fields["work_mode"], "remote")
        job_fields["work_mode"] = "remote"
        self.processor.fix_work_mode_fields(job_fields)
        self.assertEqual(job_fields["work_mode"], "remote")

    def test_normalize_integration(self):
        self.assertEqual(self.processor.normalize(" Café-Doce. "), "cafedoce")
        self.assertEqual(self.processor.normalize("Árvore"), "arvore")
        self.assertEqual(self.processor.normalize(123), 123)

    def test_full_job_fields_integration(self):
        job_fields = self.default_job_fields.copy()
        self.processor.fix_schedule_fields(job_fields)
        self.processor.fix_type_of_applicant_fields(job_fields)
        self.processor.fix_work_mode_fields(job_fields)
        self.assertEqual(job_fields['company'], 'Company David')
        self.assertIn(job_fields['work_mode'], ['remote', 'on-site', 'hybrid'])
        self.assertEqual(job_fields['type_of_applicant'], 'Public')
        self.assertEqual(job_fields['schedule_type'].lower(), 'full-time')
        self.assertEqual(job_fields['amount'], '1400€')
        self.assertEqual(job_fields['benefits'], 'Acesso a seguro de saúde e eventos de team-building')
        self.assertEqual(job_fields['teams_amount'], '2')
        self.assertEqual(job_fields['team_ids'], '2')
        self.assertEqual(job_fields['start_date_full_time'], '01/08/2025')
        self.assertEqual(job_fields['end_date_full_time'], '31/10/2025')
        self.assertEqual(job_fields['vacancies_full_time'], '2')
        self.assertEqual(job_fields['geo_radius'], '25')
        self.assertEqual(job_fields['lat'], '')
        self.assertEqual(job_fields['lng'], '')
        self.assertEqual(job_fields['pin_code'], '')
        self.assertEqual(job_fields['shifts'], '')
        self.assertEqual(job_fields['shift_name'], '')
        self.assertEqual(job_fields['start_date_shift'], '')
        self.assertEqual(job_fields['end_date_shift'], '')
        self.assertEqual(job_fields['vacancies_shift'], '')
        self.assertEqual(job_fields['custom_shift_name'], '')
        self.assertEqual(job_fields['start_date_custom'], '')
        self.assertEqual(job_fields['end_date_custom'], '')
        self.assertEqual(job_fields['vacancies_custom'], '')

if __name__ == '__main__':
    unittest.main()
