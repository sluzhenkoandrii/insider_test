from selenium.webdriver.common.by import By

from ui_test_project.utils.config_helper import config
from .base_page import BasePage


class CareersPage(BasePage):
    # Locators of the Careers page
    LOCATIONS_BLOCK = (By.ID, "career-our-location")
    TEAMS_BLOCK = (By.ID, "career-find-our-calling")
    LIFE_AT_INSIDER_BLOCK = (By.XPATH, "//h2[contains(text(), 'Life at Insider')]//ancestor::section")
    SEE_ALL_JOBS_BUTTON = (By.XPATH, "//a[contains(text(), 'See all QA jobs')]")

    def __init__(self, selenium) -> None:
        super().__init__(selenium)
        self.selenium = selenium
        self.qa_careers_url = f"{config['use_insider_url']}careers/quality-assurance/"

    def is_careers_page_loaded(self) -> bool:
        # Check if all the items are visible
        return all([
            self.is_element_visible(self.selenium, *self.LOCATIONS_BLOCK),
            self.is_element_visible(self.selenium, *self.TEAMS_BLOCK),
            self.is_element_visible(self.selenium, *self.LIFE_AT_INSIDER_BLOCK)
        ])

    def go_to_qa_jobs(self) -> None:
        # Navigate to needed page through page URL
        self.selenium.get(self.qa_careers_url)
        self.wait_to_be_clickable(self.selenium, *self.SEE_ALL_JOBS_BUTTON).click()
