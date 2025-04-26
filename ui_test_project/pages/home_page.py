from selenium.webdriver.common.by import By

from ui_test_project.utils.config_helper import config
from .base_page import BasePage


class HomePage(BasePage):
    # Locators of the main page
    ACCEPT_COOKIES_BUTTON = (By.ID, "wt-cli-accept-all-btn")
    COMPANY_MENU = (By.XPATH, "//a[normalize-space()='Company']")
    CAREERS_LINK = (By.XPATH, "//a[text()='Careers']")

    def __init__(self, selenium) -> None:
        super().__init__(selenium)

    @staticmethod
    def navigate_to_main_page(selenium) -> None:
        selenium.get(config['use_insider_url'])

    def accept_cookies(self) -> None:
        # Accept cookies
        if self.is_element_visible(self.selenium, *self.ACCEPT_COOKIES_BUTTON):
            self.wait_to_be_clickable(self.selenium, *self.ACCEPT_COOKIES_BUTTON).click()

    def navigate_to_careers(self) -> None:
        # Click on Company menu and Careers
        self.wait_to_be_clickable(self.selenium, *self.COMPANY_MENU).click()
        self.wait_to_be_clickable(self.selenium, *self.CAREERS_LINK).click()
