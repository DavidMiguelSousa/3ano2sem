import unittest
from unittest.mock import patch
from src.uni_scraper.scraper_processor import ScraperNetEmpregos
from src.interactor.flow_controller import FlowController


class TestScraperNetEmpregos(unittest.TestCase):
    
    def setUp(self):
        self.url = "https://www.net-empregos.com"
        self.scraper = ScraperNetEmpregos(self.url)
    
    def tearDown(self):
        if hasattr(self.scraper, 'driver') and self.scraper.driver:
            self.scraper.close_driver()
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    @patch.object(FlowController, "extract_job_fields")
    def test_complete_scraping_workflow_success(self, mock_extract_fields, mock_safe_get):
        # Arrange
        listing_html = """
        <html>
            <body>
                <div class="listSearchResult">
                    <article>
                        <a href="/ofertas/123/python-developer">Python Developer</a>
                        <span>TechCorp</span>
                        <span>Lisboa</span>
                    </article>
                    <article>
                        <a href="/ofertas/124/data-scientist">Data Scientist</a>
                        <span>DataLab</span>
                        <span>Porto</span>
                    </article>
                </div>
            </body>
        </html>
        """
        
        job_html_1 = """
        <html>
            <body>
                <h1>Python Developer - Full Time</h1>
                <a class="oferta-link">Lisboa, Portugal</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Seeking experienced Python developer for full-time position. 
                    Requirements: 3+ years Python, Django, REST APIs. 
                    Remote work available. Competitive salary and benefits package.</p>
                </div>
            </body>
        </html>
        """
        
        job_html_2 = """
        <html>
            <body>
                <h1>Data Scientist - Machine Learning</h1>
                <a class="oferta-link">Porto, Portugal</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Data scientist position focusing on machine learning models. 
                    Part-time position available. Requires Python, TensorFlow, SQL knowledge.</p>
                </div>
            </body>
        </html>
        """
        
        mock_safe_get.side_effect = [listing_html, job_html_1, job_html_2]
        
        mock_extract_fields.side_effect = [
            {
                "job_title": "Python Developer",
                "location": "Lisboa",
                "work_mode": "Remote",
                "schedule_type": "Full-time",
                "experience_required": "3+ years"
            },
            {
                "job_title": "Data Scientist", 
                "location": "Porto",
                "work_mode": "On-site",
                "schedule_type": "Part-time",
                "skills": ["Python", "TensorFlow", "SQL"]
            }
        ]
        
        # Act
        results = self.scraper.scrape()
        
        # Assert
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        
        # Verify first job result
        job_1 = results[0]
        self.assertIn("job_fields", job_1)
        self.assertIn("source_link", job_1)
        self.assertEqual(job_1["source_link"], "https://www.net-empregos.com/ofertas/123/python-developer")
        self.assertEqual(job_1["job_fields"]["job_title"], "Python Developer")
        self.assertEqual(job_1["job_fields"]["schedule_type"], "Full-time")
        
        # Verify second job result
        job_2 = results[1]
        self.assertEqual(job_2["source_link"], "https://www.net-empregos.com/ofertas/124/data-scientist")
        self.assertEqual(job_2["job_fields"]["job_title"], "Data Scientist")
        self.assertEqual(job_2["job_fields"]["schedule_type"], "Part-time")
        
        self.assertEqual(mock_extract_fields.call_count, 2)
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    def test_empty_listing_page_handling(self, mock_safe_get):
        # Arrange
        empty_html = """
        <html>
            <body>
                <div class="listSearchResult">
                    <!-- No job listings -->
                </div>
            </body>
        </html>
        """
        
        mock_safe_get.return_value = empty_html
        
        # Act
        results = self.scraper.scrape()
        
        # Assert
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    def test_malformed_html_handling(self, mock_safe_get):
        # Arrange
        malformed_html = """
        <html>
            <body>
                <div class="different-structure">
                    <span>Not the expected format</span>
                </div>
            </body>
        </html>
        """
        
        mock_safe_get.return_value = malformed_html
        
        # Act 
        results = self.scraper.scrape()

        # Assert
        self.assertIsInstance(results, list)
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    @patch.object(FlowController, "extract_job_fields")
    def test_job_page_parsing_with_missing_elements(self, mock_extract_fields, mock_safe_get):
        # Arrange
        listing_html = """
        <html>
            <body>
                <div class="listSearchResult">
                    <article>
                        <a href="/ofertas/125/incomplete-job">Incomplete Job</a>
                    </article>
                </div>
            </body>
        </html>
        """
        
        incomplete_job_html = """
        <html>
            <body>
                <h1>Job Title Only</h1>
                <!-- Missing location and description -->
            </body>
        </html>
        """
        
        mock_safe_get.side_effect = [listing_html, incomplete_job_html]
        mock_extract_fields.return_value = {"job_title": "Incomplete Job"}
        
        # Act
        results = self.scraper.scrape()
        
        # Assert
        self.assertEqual(len(results), 1)
        job = results[0]
        self.assertIn("job_fields", job)
        self.assertIn("source_link", job)
        
        description_call = mock_extract_fields.call_args[0][0]
        self.assertIn("Título: Job Title Only", description_call)
        self.assertIn("Localização:", description_call)
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    def test_network_error_simulation(self, mock_safe_get):
        # Arrange
        mock_safe_get.side_effect = Exception("Network error")
        
        # Act & Assert
        with self.assertRaises(Exception):
            self.scraper.scrape()
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    @patch.object(FlowController, "extract_job_fields")
    def test_flow_controller_error_handling(self, mock_extract_fields, mock_safe_get):
        # Arrange
        listing_html = """
        <html>
            <body>
                <div class="listSearchResult">
                    <article>
                        <a href="/ofertas/126/error-job">Error Job</a>
                    </article>
                </div>
            </body>
        </html>
        """
        
        job_html = """
        <html>
            <body>
                <h1>Error Job</h1>
                <a class="oferta-link">Lisboa</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Job description</p>
                </div>
            </body>
        </html>
        """
        
        mock_safe_get.side_effect = [listing_html, job_html]
        mock_extract_fields.side_effect = Exception("FlowController error")
        
        # Act & Assert
        with self.assertRaises(Exception):
            self.scraper.scrape()
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    @patch.object(FlowController, "extract_job_fields")
    def test_multiple_job_listings_with_varied_content(self, mock_extract_fields, mock_safe_get):
        # Arrange
        listing_html = """
        <html>
            <body>
                <div class="listSearchResult">
                    <article>
                        <a href="/ofertas/201/senior-engineer">Senior Software Engineer</a>
                    </article>
                    <article>
                        <a href="/ofertas/202/intern-position">Marketing Intern</a>
                    </article>
                    <article>
                        <a href="/ofertas/203/manager-role">Project Manager</a>
                    </article>
                </div>
            </body>
        </html>
        """
        
        senior_engineer_html = """
        <html>
            <body>
                <h1>Senior Software Engineer</h1>
                <a class="oferta-link">Lisboa, Portugal</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Senior role requiring 5+ years experience. Full-time position with competitive salary.
                    Technologies: Java, Spring, Microservices, Docker, Kubernetes.</p>
                </div>
            </body>
        </html>
        """
        
        intern_html = """
        <html>
            <body>
                <h1>Marketing Intern</h1>
                <a class="oferta-link">Porto, Portugal</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Entry-level internship position. Part-time, 20 hours per week.
                    Great opportunity for students to gain experience in digital marketing.</p>
                </div>
            </body>
        </html>
        """
        
        manager_html = """
        <html>
            <body>
                <h1>Project Manager</h1>
                <a class="oferta-link">Coimbra, Portugal</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Experienced project manager needed for agile teams. 
                    Hybrid work model. Requires PMP certification and 3+ years experience.</p>
                </div>
            </body>
        </html>
        """
        
        mock_safe_get.side_effect = [listing_html, senior_engineer_html, intern_html, manager_html]
        
        mock_extract_fields.side_effect = [
            {
                "job_title": "Senior Software Engineer",
                "experience_level": "Senior",
                "schedule_type": "Full-time",
                "technologies": ["Java", "Spring", "Docker"]
            },
            {
                "job_title": "Marketing Intern",
                "experience_level": "Entry",
                "schedule_type": "Part-time",
                "hours_per_week": 20
            },
            {
                "job_title": "Project Manager",
                "work_mode": "Hybrid",
                "certifications_required": ["PMP"],
                "experience_required": "3+ years"
            }
        ]
        
        # Act
        results = self.scraper.scrape()
        
        # Assert
        self.assertEqual(len(results), 3)
        
        job_titles = [job["job_fields"]["job_title"] for job in results]
        self.assertIn("Senior Software Engineer", job_titles)
        self.assertIn("Marketing Intern", job_titles)
        self.assertIn("Project Manager", job_titles)
        
        for job in results:
            self.assertTrue(job["source_link"].startswith("https://www.net-empregos.com/ofertas/"))
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    @patch.object(FlowController, "extract_job_fields")
    def test_unicode_and_special_characters_handling(self, mock_extract_fields, mock_safe_get):
        # Arrange
        listing_html = """
        <html>
            <body>
                <div class="listSearchResult">
                    <article>
                        <a href="/ofertas/301/dev-português">Desenvolvedor Sênior</a>
                    </article>
                </div>
            </body>
        </html>
        """
        
        portuguese_job_html = """
        <html>
            <body>
                <h1>Desenvolvedor Sênior - Programação</h1>
                <a class="oferta-link">São Paulo, Brasil</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Posição para desenvolvedor sênior com experiência em programação avançada.
                    Requisitos: graduação, português fluente, conhecimento em tecnologias modernas.
                    Benefícios incluem plano de saúde e férias remuneradas.</p>
                </div>
            </body>
        </html>
        """
        
        mock_safe_get.side_effect = [listing_html, portuguese_job_html]
        mock_extract_fields.return_value = {
            "job_title": "Desenvolvedor Sênior",
            "language_requirements": "Português fluente",
            "benefits": "Plano de saúde, férias remuneradas"
        }
        
        # Act
        results = self.scraper.scrape()
        
        # Assert
        self.assertEqual(len(results), 1)
        job = results[0]
        self.assertEqual(job["job_fields"]["job_title"], "Desenvolvedor Sênior")
        self.assertIn("português", job["job_fields"]["language_requirements"].lower())
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    @patch.object(FlowController, "extract_job_fields")
    def test_edge_case_large_number_of_jobs(self, mock_extract_fields, mock_safe_get):
        articles = []
        for i in range(50):
            articles.append(f'<article><a href="/ofertas/{i}/job-{i}">Job {i}</a></article>')
        
        listing_html = f"""
        <html>
            <body>
                <div class="listSearchResult">
                    {''.join(articles)}
                </div>
            </body>
        </html>
        """
        
        # Simple job page
        job_html = """
        <html>
            <body>
                <h1>Test Job</h1>
                <a class="oferta-link">Lisboa</a>
                <div class="job-description mb-40 dont-break-out">
                    <p>Test description</p>
                </div>
            </body>
        </html>
        """
        
        mock_responses = [listing_html] + [job_html] * 50
        mock_safe_get.side_effect = mock_responses
        
        mock_extract_fields.return_value = {"job_title": "Test Job"}
        
        # Act
        results = self.scraper.scrape()
        
        # Assert
        self.assertEqual(len(results), 50)
        self.assertEqual(mock_extract_fields.call_count, 50)
    
    def test_driver_initialization_and_cleanup(self):
        # This test doesn't mock anything to verify actual driver behavior
        scraper = ScraperNetEmpregos("https://www.net-empregos.com")
        
        # Verify driver is initialized
        self.assertIsNotNone(scraper.driver)
        
        # Verify cleanup works
        scraper.close_driver()
        
    
    @patch.object(ScraperNetEmpregos, "safe_get")
    @patch.object(FlowController, "extract_job_fields")
    def test_job_fields_extraction_integration(self, mock_extract_fields, mock_safe_get):
        # Arrange
        listing_html = """
        <html>
            <body>
                <div class="listSearchResult">
                    <article>
                        <a href="/ofertas/400/complex-job">Complex Job Analysis</a>
                    </article>
                </div>
            </body>
        </html>
        """
        
        complex_job_html = """
        <html>
            <body>
                <h1>Senior Data Analyst - Remote Position</h1>
                <a class="oferta-link">Lisboa, Portugal (Remote)</a>
                <div class="job-description mb-40 dont-break-out">
                    <p><strong>Company:</strong> TechCorp International</p>
                    <p><strong>Position:</strong> Senior Data Analyst</p>
                    <p><strong>Type:</strong> Full-time, Remote work</p>
                    <p><strong>Requirements:</strong></p>
                    <ul>
                        <li>5+ years of experience in data analysis</li>
                        <li>Proficiency in Python, SQL, Tableau</li>
                        <li>Experience with machine learning frameworks</li>
                        <li>Bachelor's degree in relevant field</li>
                    </ul>
                    <p><strong>Benefits:</strong> Health insurance, flexible schedule, professional development budget</p>
                </div>
            </body>
        </html>
        """
        
        mock_safe_get.side_effect = [listing_html, complex_job_html]
        
        def check_description(description):
            self.assertIn("Senior Data Analyst - Remote Position", description)
            self.assertIn("Lisboa, Portugal (Remote)", description)
            self.assertIn("TechCorp International", description)
            self.assertIn("5+ years of experience", description)
            self.assertIn("Python, SQL, Tableau", description)
            return {"job_title": "Senior Data Analyst", "work_mode": "Remote"}
        
        mock_extract_fields.side_effect = check_description
        
        # Act
        results = self.scraper.scrape()
        
        # Assert
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["job_fields"]["job_title"], "Senior Data Analyst")


if __name__ == '__main__':
    unittest.main()
