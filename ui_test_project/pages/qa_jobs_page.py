from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .base_page import BasePage


class QAJobsPage(BasePage):
    # Locators of the QA Jobs page
    LOCATION_FILTER = (By.ID, "select2-filter-by-location-container")
    DEPARTMENT_FILTER = (By.ID, "select2-filter-by-department-container")
    ISTANBUL_OPTION = (
        By.XPATH, "//select[@id='filter-by-location']/option[contains(text(), 'Istanbul, Turkey')]"
    )
    QA_DEPARTMENT_OPTION = (
        By.XPATH, "//select[@id='filter-by-department']/option[contains(text(), 'Quality Assurance')]"
    )
    JOB_POSITIONS = (By.CSS_SELECTOR, ".position-list-item")
    POSITION_TITLE = (By.CSS_SELECTOR, ".position-title")
    DEPARTMENT_TEXT = (By.CSS_SELECTOR, ".position-department")
    LOCATION_TEXT = (By.CSS_SELECTOR, ".position-location")
    VIEW_ROLE_BUTTON = (By.XPATH, "//a[contains(text(), 'View Role')]")
    ALL_LOCATIONS = (By.CSS_SELECTOR, ".select2-results__option")
    FILTER_OPTIONS = (By.CSS_SELECTOR, ".select2-results")

    def wait_until_be_returned_the_options(self, filter_by) -> None:
        # open, check and close filter drop-down to wait until BE return the options
        location_filter = self.wait_visibility(self.selenium, *filter_by)

        for _ in range(10):
            location_filter.click()
            if len(self.wait_elements_visibility(self.selenium, *self.ALL_LOCATIONS)) < 2:
                sleep(2)  # waiting time of each iteration (could be moved to config)
                location_filter.click()
                self.wait_invisibility(*self.FILTER_OPTIONS)
            else:
                return

    def filter_by_location_or_departament(self, filter_by, filter_value) -> None:
        # set needed value to the filter accordingly to specified selector
        self.wait_until_be_returned_the_options(filter_by)

        locations_list = self.wait_elements_visibility(self.selenium, *self.ALL_LOCATIONS)
        for location in range(len(locations_list)):
            if locations_list[location].text == filter_value:
                ActionChains(self.selenium).move_to_element(locations_list[location]).click().perform()
                break

    def get_job_listings(self):
        """
        Forced scroll using JavaScript to the first vacancy and return all available.
        """
        # scroll down using JavaScript to jobs elements apper in DOM
        self.selenium.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

        # find first element to perform scrolling
        first_job_position = self.wait_visibility(self.selenium, *self.JOB_POSITIONS)
        self.selenium.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_job_position)
        sleep(0.5)  # needed to wait until scrolling is finished

        return self.wait_elements_visibility(self.selenium, *self.JOB_POSITIONS)

    def verify_job_details(self, job_element, expected_title, expected_department, expected_location) -> None:
        title = job_element.find_element(*self.POSITION_TITLE).text
        department = job_element.find_element(*self.DEPARTMENT_TEXT).text
        location = job_element.find_element(*self.LOCATION_TEXT).text

        assert expected_title in title, f"Title mismatch: expected '{expected_title}' in '{title}'"
        assert expected_department in (
            department, f"Department mismatch: expected '{expected_department}' in '{department}'")
        assert expected_location in (
            location, f"Location mismatch: expected '{expected_location}' in '{location}'")

    def click_view_role_and_switch_to_new_tab(self) -> None:
        jobs = self.wait_elements_visibility(self.selenium, *self.JOB_POSITIONS)

        for job in range(len(jobs)):
            ActionChains(self.selenium).move_to_element(jobs[job]).perform()
            break
        self.wait_to_be_clickable(self.selenium, *self.VIEW_ROLE_BUTTON).click()

        WebDriverWait(self.selenium, 10).until(
            lambda d: len(d.window_handles) > 1
        )
        self.selenium.switch_to.window(self.selenium.window_handles[-1])

    def close_new_tab_and_return(self) -> None:
        self.selenium.close()
        self.selenium.switch_to.window(self.selenium.window_handles[0])
