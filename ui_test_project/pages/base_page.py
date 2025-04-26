from selenium.webdriver.support.expected_conditions import (visibility_of_element_located as visible,
                                                            invisibility_of_element_located as invisible,
                                                            text_to_be_present_in_element as text_present,
                                                            element_to_be_clickable, presence_of_element_located)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from ui_test_project.utils.config_helper import config


class BasePage:
    def __init__(self, selenium):
        self.selenium = selenium
        self.wait = WebDriverWait(selenium, config['time_to_wait_for_el'])

    def wait_to_be_clickable(self, selenium, by, selector):
        """Wait for the DOM element specified to become clickable and return it."""
        self.wait.until(element_to_be_clickable((by, selector)))
        return selenium.find_element(by, selector)

    def wait_presents(self, selenium, by, selector):
        """Wait for the DOM element specified to become visible and return it."""
        self.wait.until(presence_of_element_located((by, selector)))
        return selenium.find_element(by, selector)

    def wait_elements_visibility(self, selenium, by, selector):
        """Wait for the DOM element specified to become visible and return it."""
        self.wait.until(visible((by, selector)))
        return selenium.find_elements(by, selector)

    def wait_visibility(self, selenium, by, selector):
        """Wait for the DOM element specified to become visible and return it."""
        self.wait.until(visible((by, selector)))
        return selenium.find_element(by, selector)

    def wait_invisibility(self, by, selector):
        """Wait for the DOM element specified to become invisible."""
        self.wait.until(invisible((by, selector)))

    def wait_matching_text(self, by, selector, text):
        """Wait for the DOM element specified to match specific text."""
        self.wait.until(text_present((by, selector), text))

    def is_element_visible(self, selenium, by, selector) -> bool:
        """Return True if element is visible and False when not"""
        try:
            self.wait_visibility(selenium, by, selector)
            return True
        except TimeoutException:
            return False

