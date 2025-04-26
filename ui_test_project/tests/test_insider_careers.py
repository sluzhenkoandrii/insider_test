from ui_test_project.pages.home_page import HomePage
from ui_test_project.pages.careers_page import CareersPage
from ui_test_project.pages.qa_jobs_page import QAJobsPage


class TestInsiderCareers:

    def test_insider_qa_positions(self, selenium, test_failed_check):
        # 1. Visit Insider homepage and verify it's opened
        home_page = HomePage(selenium)
        home_page.navigate_to_main_page(selenium)
        home_page.accept_cookies()
        assert "Insider" in selenium.title, "Homepage is not opened"

        # 2. Navigate to Careers page through Company menu and verify its sections
        home_page.navigate_to_careers()
        careers_page = CareersPage(selenium)
        assert careers_page.is_careers_page_loaded(), "Careers page sections are not loaded properly"

        # 3. Navigate directly to QA jobs page and apply filters
        careers_page.go_to_qa_jobs()
        qa_jobs_page = QAJobsPage(selenium)
        qa_jobs_page.filter_by_location_or_departament(
            qa_jobs_page.LOCATION_FILTER, 'Istanbul, Turkiye'
        )
        qa_jobs_page.filter_by_location_or_departament(
            qa_jobs_page.DEPARTMENT_FILTER, 'Quality Assurance'
        )

        # Verify job listings
        assert len(qa_jobs_page.get_job_listings()) > 0, "No job listings found"

        # 4. Verify each job's details
        job_listings = qa_jobs_page.get_job_listings()
        for job in job_listings:
            qa_jobs_page.verify_job_details(
                job_element=job,
                expected_title="Quality Assurance",
                expected_department="Quality Assurance",
                expected_location="Istanbul, Turkiye"
            )

        # 5. Click View Role and verify redirect
        qa_jobs_page.click_view_role_and_switch_to_new_tab()
        assert "lever.co" in selenium.current_url, "Not redirected to Lever application form"

        qa_jobs_page.close_new_tab_and_return()
