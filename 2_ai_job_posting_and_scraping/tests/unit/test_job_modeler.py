import unittest

from src.job_modeler import JobModelFromBot, JobModelFromScraper

class TestJobModelFromBot(unittest.TestCase):
    def test_valid_transformation(self):
        input_data = {
            'job_title': 'Engenheiro de Software',
            'degree_of_specialization': 'Non-specialized',
            'work_area': 'Catering',
            'job_description': 'Desenvolvimento de software.',
            'work_mode': 'Remote',
            'job_address': 'Rua Exemplo, 123',
            'job_country': 'Portugal',
            'job_city': 'Lisboa',
            'district': 'Lisboa',
            'lat': '38.7223',
            'lng': '-9.1393',
            'pin_code': '1000-000',
            'geo_radius': '50',
            'schedule_type': 'Full-Time',
            'start_date_full_time': '2024-09-01',
            'end_date_full_time': '2025-09-01',
            'vacancies_full_time': '2',
            'payment_frequency': 'Monthly',
            'amount': '1200',
            'how_to_pay_student': 'Green Receipts',
            'type_of_applicant': 'Public',
            'benefits': 'Subsídio de alimentação',
            'team_Ids': '1',
            'location_id': 'Lisboa',
        }
        model = JobModelFromBot(input_data)
        job = model.to_dict()
        self.assertEqual(job['job_title'], 'Engenheiro de Software')
        self.assertEqual(job['degree_of_specialization'], 'non-specialized')
        self.assertIsInstance(job['area_of_work_id'], int)
        self.assertEqual(job['job_description'], 'Desenvolvimento de software.')
        self.assertEqual(job['work_mode'], 'remote')
        self.assertIn('Lisboa', job['job_address'])
        self.assertEqual(job['job_latitude'], 38.7223)
        self.assertEqual(job['job_longitude'], -9.1393)
        self.assertEqual(job['post_code'], '1000-000')
        self.assertEqual(job['geofencing_radius'], 50)
        self.assertEqual(job['schedule_type'], 'full-time')
        self.assertEqual(job['payment_frequency'], 'monthly')
        self.assertEqual(job['amount'], 1200.0)
        self.assertEqual(job['type_of_applicant'], 'public')
        self.assertEqual(job['benefits'], 'Subsídio de alimentação')
        self.assertEqual(job['location_id']['label'], 'Lisboa')
        self.assertIsInstance(job['location_id']['value'], int)
        self.assertIsInstance(job['how_to_pay_student'], list)
        self.assertEqual(job['how_to_pay_student'][0]['label'], 'Green Receipts')
        self.assertEqual(job['teams'], '1')
        self.assertIsInstance(job['schedule'], str)
        self.assertEqual(job['job_start_date'], '2024-09-01')
        self.assertEqual(job['job_end_date'], '2025-09-01')

    def test_each_field_isolated(self):
        # Testa cada campo isoladamente
        fields = [
            ('job_title', 'Engenheiro de Software', lambda job: self.assertEqual(job['job_title'], 'Engenheiro de Software')),
            ('degree_of_specialization', 'Non-specialized', lambda job: self.assertEqual(job['degree_of_specialization'], 'non-specialized')),
            ('work_area', 'Catering', lambda job: self.assertIsInstance(job['area_of_work_id'], int)),
            ('job_description', 'Desenvolvimento de software.', lambda job: self.assertEqual(job['job_description'], 'Desenvolvimento de software.')),
            ('work_mode', 'Remote', lambda job: self.assertEqual(job['work_mode'], 'remote')),
            ('job_address', 'Rua Exemplo, 123', lambda job: self.assertIn('Rua Exemplo, 123', job['job_address'])),
            ('job_country', 'Portugal', lambda job: self.assertIn('Portugal', job['job_address'])),
            ('job_city', 'Lisboa', lambda job: self.assertIn('Lisboa', job['job_address'])),
            ('district', 'Lisboa', lambda job: self.assertIsNone(job.get('district'))),
            ('lat', '38.7223', lambda job: self.assertEqual(job['job_latitude'], 38.7223)),
            ('lng', '-9.1393', lambda job: self.assertEqual(job['job_longitude'], -9.1393)),
            ('pin_code', '1000-000', lambda job: self.assertEqual(job['post_code'], '1000-000')),
            ('geo_radius', '50', lambda job: self.assertEqual(job['geofencing_radius'], 50)),
            ('schedule_type', 'Full-Time', lambda job: self.assertEqual(job['schedule_type'], 'full-time')),
            ('start_date_full_time', '2024-09-01', lambda job: self.assertEqual(job['job_start_date'], '2024-09-01')),
            ('end_date_full_time', '2025-09-01', lambda job: self.assertEqual(job['job_end_date'], '2025-09-01')),
            ('payment_frequency', 'Monthly', lambda job: self.assertEqual(job['payment_frequency'], 'monthly')),
            ('amount', '1200', lambda job: self.assertEqual(job['amount'], 1200.0)),
            ('how_to_pay_student', 'Green Receipts', lambda job: self.assertEqual(job['how_to_pay_student'][0]['label'], 'Green Receipts')),
            ('type_of_applicant', 'Public', lambda job: self.assertEqual(job['type_of_applicant'], 'public')),
            ('benefits', 'Subsídio de alimentação', lambda job: self.assertEqual(job['benefits'], 'Subsídio de alimentação')),
            ('team_Ids', '1', lambda job: self.assertEqual(job['teams'], '1')),
            ('location_id', 'Lisboa', lambda job: self.assertEqual(job['location_id']['label'], 'Lisboa')),
        ]
        for field, value, assertion in fields:
            with self.subTest(field=field):
                input_data = {field: value}
                model = JobModelFromBot(input_data)
                job = model.to_dict()
                assertion(job)

    def test_missing_optional_fields(self):
        input_data = {
            'job_title': 'Designer',
            'degree_of_specialization': 'Specialized',
            'work_area': 'Bar Service',
            'job_description': 'Criação de artes gráficas.'
        }
        model = JobModelFromBot(input_data)
        job = model.to_dict()
        self.assertEqual(job['job_title'], 'Designer')
        self.assertEqual(job['degree_of_specialization'], 'specialized')
        self.assertIsInstance(job['area_of_work_id'], int)
        self.assertEqual(job['job_description'], 'Criação de artes gráficas.')
        self.assertIsNone(job.get('job_city'))
        self.assertIsNone(job.get('benefits'))
        print(f"Test missing optional fields passed: {job}")
        
    def test_no_fields(self):
        input_data = {
            'job_title': '',
            'degree_of_specialization': '',
            'work_area': '',
            'job_description': '',
            'work_mode': '',
            'job_address': '',
            'job_country': '',
            'job_city': '',
            'district': '',
            'lat': '',
            'lng': '',
            'pin_code': '',
            'geo_radius': '',
            'schedule_type': '',
            'start_date_full_time': '',
            'end_date_full_time': '',
            'vacancies_full_time': '',
            'payment_frequency': '',
            'amount': '',
            'how_to_pay_student': '',
            'type_of_applicant': '',
            'benefits': '',
            'team_Ids': '',
            'location_id': '',
        }
        model = JobModelFromBot(input_data)
        job = model.to_dict()
        self.assertEqual(job['job_title'], '')
        self.assertEqual(job['degree_of_specialization'], None)
        self.assertIsInstance(job['area_of_work_id'], int)
        self.assertEqual(job['job_description'], '')
        self.assertEqual(job['work_mode'], None)
        self.assertEqual(job['job_address'], '')
        self.assertEqual(job['job_latitude'], None)
        self.assertEqual(job['job_longitude'], None)
        self.assertEqual(job['post_code'], '')
        self.assertEqual(job['geofencing_radius'], 50)
        self.assertEqual(job['schedule_type'], None)
        self.assertEqual(job['payment_frequency'], None)
        self.assertEqual(job['amount'], None)
        self.assertEqual(job['type_of_applicant'], '')
        self.assertEqual(job['benefits'], '')
        self.assertEqual(job['location_id'], {'label': '', 'value': 0})
        self.assertIsInstance(job['how_to_pay_student'], list)
        self.assertEqual(job['how_to_pay_student'], [])
        self.assertEqual(job['teams'], '')
        self.assertIsInstance(job['schedule'], str)
        self.assertEqual(job['job_start_date'], None)
        self.assertEqual(job['job_end_date'], None)
        
        
        print(f"Test no fields passed: {job}")

    def test_individual_fields(self):
        test_cases = [
            ('job_title', 'Engenheiro de Software', lambda job: self.assertEqual(job['job_title'], 'Engenheiro de Software')),
            ('degree_of_specialization', 'Non-specialized', lambda job: self.assertEqual(job['degree_of_specialization'], 'non-specialized')),
            ('work_area', 'Catering', lambda job: self.assertIsInstance(job['area_of_work_id'], int)),
            ('job_description', 'Desenvolvimento de software.', lambda job: self.assertEqual(job['job_description'], 'Desenvolvimento de software.')),
            ('work_mode', 'Remote', lambda job: self.assertEqual(job['work_mode'], 'remote')),
            ('job_address', 'Rua Exemplo, 123', lambda job: self.assertIn('Rua Exemplo, 123', job['job_address'])),
            ('job_country', 'Portugal', lambda job: self.assertIn('Portugal', job['job_address'])),
            ('job_city', 'Lisboa', lambda job: self.assertIn('Lisboa', job['job_address'])),
            ('district', 'Lisboa', lambda job: self.assertIsNone(job.get('district'))),
            ('lat', '38.7223', lambda job: self.assertEqual(job['job_latitude'], 38.7223)),
            ('lng', '-9.1393', lambda job: self.assertEqual(job['job_longitude'], -9.1393)),
            ('pin_code', '1000-000', lambda job: self.assertEqual(job['post_code'], '1000-000')),
            ('geo_radius', '50', lambda job: self.assertEqual(job['geofencing_radius'], 50)),
            ('schedule_type', 'Full-Time', lambda job: self.assertEqual(job['schedule_type'], 'full-time')),
            ('start_date_full_time', '2024-09-01', lambda job: self.assertEqual(job['job_start_date'], '2024-09-01')),
            ('end_date_full_time', '2025-09-01', lambda job: self.assertEqual(job['job_end_date'], '2025-09-01')),
            ('vacancies_full_time', '2', lambda job: self.assertIn('vacancies', job['schedule'])),
            ('payment_frequency', 'Monthly', lambda job: self.assertEqual(job['payment_frequency'], 'monthly')),
            ('amount', '1200', lambda job: self.assertEqual(job['amount'], 1200.0)),
            ('how_to_pay_student', 'Green Receipts', lambda job: self.assertEqual(job['how_to_pay_student'][0]['label'], 'Green Receipts')),
            ('type_of_applicant', 'Public', lambda job: self.assertEqual(job['type_of_applicant'], 'public')),
            ('benefits', 'Subsídio de alimentação', lambda job: self.assertEqual(job['benefits'], 'Subsídio de alimentação')),
            ('team_Ids', '1', lambda job: self.assertEqual(job['teams'], '1')),
            ('location_id', 'Lisboa', lambda job: self.assertEqual(job['location_id']['label'], 'Lisboa')),
        ]
            
        for field, value, assertion in test_cases:
            with self.subTest(field=field):
                input_data = {field: value}
                model = JobModelFromBot(input_data)
                job = model.to_dict()
                assertion(job)
            
        print(f"Test individual field '{field}' passed: {job}")

class TestJobModelFromScraper(unittest.TestCase):
    def test_schedule_formatting(self):
        input_data = {
            'job_title': 'Analista de Dados',
            'degree_of_specialization': 'Specialized',
            'work_area': 'Tutoring',
            'job_description': 'Análise de dados.',
            'work_mode': 'Remote',
            'job_address': 'Rua dos Dados, 1',
            'job_country': 'Portugal',
            'job_city': 'Porto',
            'district': 'Porto',
            'lat': '41.1579',
            'lng': '-8.6291',
            'pin_code': '4000-000',
            'geo_radius': '30',
            'schedule_type': 'Part-Time',
            'start_date_full_time': '2024-10-01',
            'end_date_full_time': '2024-12-31',
            'vacancies_full_time': '3',
            'payment_frequency': 'Hourly',
            'amount': '1000',
            'how_to_pay_student': 'Employment Contract',
            'type_of_applicant': 'Team-only',
            'benefits': 'Computador',
            'location_id': 'Porto',
        }
        model = JobModelFromScraper(input_data)
        job = model.to_dict()
        self.assertEqual(job['jobTitle'], 'Analista de Dados')
        self.assertEqual(job['degreeOfSpecialization']['name'], 'Specialized')
        self.assertEqual(job['workMode']['name'], 'Remote')
        self.assertEqual(job['jobAddress'], 'Rua dos Dados, 1')
        self.assertEqual(job['lat'], 41.1579)
        self.assertEqual(job['lng'], -8.6291)
        self.assertEqual(job['district']['name'], 'Porto')
        self.assertEqual(job['geoRadius'], 30)
        self.assertEqual(job['scheduleType']['name'], 'Weekly')
        self.assertEqual(job['fullAddress']['country'], 'Portugal')
        self.assertEqual(job['fullAddress']['city'], 'Porto')
        self.assertEqual(job['fullAddress']['zipCode'], '4000-000')
        self.assertEqual(job['fullTime']['startDate'], None)
        self.assertEqual(job['fullTime']['endDate'], None)
        self.assertEqual(job['fullTime']['vacancies'], 1)
        self.assertEqual(job['payment_frequency']['name'], 'Hourly')
        self.assertEqual(job['amount'], '1000')
        self.assertEqual(job['benefits'], 'Computador')
        self.assertIsInstance(job['how_to_pay_student'], list)
        self.assertEqual(job['how_to_pay_student'][0]['name'], 'Employment Contract')
        self.assertEqual(job['type_of_applicant']['name'], 'Team-only')
        
        print(f"Test schedule formatting passed: {job}")

    def test_individual_fields(self):
        test_cases = [
            ('job_title', 'Analista de Dados', lambda job: self.assertEqual(job['jobTitle'], 'Analista de Dados')),
            ('degree_of_specialization', 'Specialized', lambda job: self.assertEqual(job['degreeOfSpecialization']['name'], 'Specialized')),
            ('work_area', 'Tutoring', lambda job: self.assertEqual(job['areaOfWorkId']['name'], 'Tutoring')),
            ('job_description', 'Análise de dados.', lambda job: self.assertEqual(job['jobDescription'], 'Análise de dados.')),
            ('work_mode', 'Remote', lambda job: self.assertEqual(job['workMode']['name'], 'Remote')),
            ('job_address', 'Rua dos Dados, 1', lambda job: self.assertEqual(job['jobAddress'], 'Rua dos Dados, 1')),
            ('job_country', 'Portugal', lambda job: self.assertEqual(job['fullAddress']['country'], 'Portugal')),
            ('job_city', 'Porto', lambda job: self.assertEqual(job['fullAddress']['city'], 'Porto')),
            ('district', 'Porto', lambda job: self.assertEqual(job['district']['name'], 'Porto')),
            ('lat', '41.1579', lambda job: self.assertEqual(job['lat'], 41.1579)),
            ('lng', '-8.6291', lambda job: self.assertEqual(job['lng'], -8.6291)),
            ('pin_code', '4000-000', lambda job: self.assertEqual(job['fullAddress']['zipCode'], '4000-000')),
            ('geo_radius', '30', lambda job: self.assertEqual(job['geoRadius'], 30)),
            ('schedule_type', 'Part-Time', lambda job: self.assertEqual(job['scheduleType']['name'], 'Weekly')),
            ('start_date_full_time', '2024-10-01', lambda job: self.assertIsNone(job['fullTime']['startDate'])),
            ('end_date_full_time', '2024-12-31', lambda job: self.assertIsNone(job['fullTime']['endDate'])),
            ('vacancies_full_time', '3', lambda job: self.assertEqual(job['fullTime']['vacancies'], 1)),
            ('payment_frequency', 'Hourly', lambda job: self.assertEqual(job['payment_frequency']['name'], 'Hourly')),
            ('amount', '1000', lambda job: self.assertEqual(job['amount'], '1000')),
            ('how_to_pay_student', 'Employment Contract', lambda job: self.assertEqual(job['how_to_pay_student'][0]['name'], 'Employment Contract')),
            ('type_of_applicant', 'Team-only', lambda job: self.assertEqual(job['type_of_applicant']['name'], 'Team-only')),
            ('benefits', 'Computador', lambda job: self.assertEqual(job['benefits'], 'Computador')),
            ('location_id', 'Porto', lambda job: self.assertTrue('areaOfWorkId' in job)),
        ]
        for field, value, assertion in test_cases:
            with self.subTest(field=field):
                input_data = {field: value}
                model = JobModelFromScraper(input_data)
                job = model.to_dict()
                assertion(job)
        print(f"Test individual field '{field}' passed: {job}")
        
    def test_no_fields(self):
        input_data = {
            'job_title': '',
            'degree_of_specialization': '',
            'work_area': '',
            'job_description': '',
            'work_mode': '',
            'job_address': '',
            'job_country': '',
            'job_city': '',
            'district': '',
            'lat': '',
            'lng': '',
            'pin_code': '',
            'geo_radius': '',
            'schedule_type': '',
            'start_date_full_time': '',
            'end_date_full_time': '',
            'vacancies_full_time': '',
            'payment_frequency': '',
            'amount': '',
            'how_to_pay_student': '',
            'type_of_applicant': '',
            'benefits': '',
            'location_id': '',
        }
        model = JobModelFromScraper(input_data)
        job = model.to_dict()
        self.assertEqual(job['jobTitle'], '')
        self.assertEqual(job['degreeOfSpecialization'], {'code': '', 'name': ''})
        self.assertEqual(job['areaOfWorkId'], {'code': 0, 'name': ''})
        self.assertEqual(job['jobDescription'], '')
        self.assertEqual(job['workMode'], {'code': '', 'name': ''})
        self.assertEqual(job['jobAddress'], '')
        self.assertEqual(job['lat'], None)
        self.assertEqual(job['lng'], None)
        self.assertEqual(job['district'], {'code': 0, 'name': ''})
        self.assertEqual(job['geoRadius'], 50)
        self.assertEqual(job['scheduleType'], {'code': None, 'name': None})
        self.assertEqual(job['fullAddress'], {'country': '', 'city': '', 'zipCode': ''})
        self.assertEqual(job['fullTime'], {'startDate': None, 'endDate': None, 'vacancies': 1})
        self.assertIsInstance(job['weekly'], list)
        self.assertIsInstance(job['customShift'], dict)
        self.assertEqual(job['payment_frequency'], {'code': '', 'name': ''})
        self.assertEqual(job['amount'], '')
        self.assertEqual(job['benefits'], '')
        self.assertEqual(job['how_to_pay_student'], [])
        self.assertEqual(job['type_of_applicant'], {'code': '', 'name': ''})
        
        print(f"Test no fields for scraper passed: {job}")
           

if __name__ == '__main__':
    unittest.main()
