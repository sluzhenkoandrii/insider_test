# import pytest
# from selenium.webdriver import ChromeOptions, FirefoxOptions
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver import Chrome, Firefox
#
#
# def pytest_addoption(parser):
#     """Add CLI options for headless mode and browser choice."""
#     parser.addoption(
#         "--headless",
#         action="store_true",
#         help="Enable headless mode for browsers"
#     )
#     parser.addoption(
#         "--browser",
#         action="store",
#         default="chrome",
#         choices=["chrome", "firefox"],
#         help="Choose browser: chrome or firefox"
#     )
#
#
# @pytest.fixture
# def browser_name(request):
#     """Return selected browser name."""
#     return request.config.getoption("browser")
#
#
# @pytest.fixture
# def headless(request):
#     """Return True if --headless is passed."""
#     return request.config.getoption("headless")
#
#
# @pytest.fixture
# def driver_options(browser_name, headless):
#     """Return browser-specific options."""
#     if browser_name == "chrome":
#         options = ChromeOptions()
#         options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
#         if headless:
#             options.add_argument("--headless=new")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--window-size=1920,1080")
#         return options
#     elif browser_name == "firefox":
#         options = FirefoxOptions()
#         if headless:
#             options.add_argument("--headless")
#         options.add_argument("--width=1920")
#         options.add_argument("--height=1080")
#         return options
#     else:
#         raise ValueError(f"Unsupported browser: {browser_name}")
#
#
# @pytest.fixture
# def selenium(selenium, browser_name):
#     """Customize selenium fixture (maximize window)."""
#     selenium.maximize_window()
#     return selenium
#
#
# @pytest.fixture(autouse=True, scope="session")
# def webdriver_manager_setup(pytestconfig):
#     """Automatically setup driver path using webdriver_manager."""
#     browser = pytestconfig.getoption("browser")
#     if browser == "chrome":
#         driver_path = ChromeDriverManager().install()
#         pytestconfig.option.driver_path = driver_path
#     elif browser == "firefox":
#         driver_path = GeckoDriverManager().install()
#         pytestconfig.option.driver_path = driver_path
#     else:
#         raise ValueError(f"Unsupported browser: {browser}")



import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    """Add CLI options."""
    group = parser.getgroup('selenium', 'selenium')
    group._addoption('--headless', action='store_true', help='Enable headless mode for supported browsers.')


@pytest.fixture
def headless(request):
    """Return True if --headless is passed."""
    return request.config.getoption('headless')


@pytest.fixture
def driver_name(request):
    """Get selected driver name from pytest-selenium."""
    return request.config.getoption('driver').lower()


@pytest.fixture
def browser_options(driver_name, headless):
    """Return browser options depending on the selected driver."""
    if driver_name == 'chrome':
        options = ChromeOptions()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if headless:
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
        return options
    elif driver_name == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        return options
    else:
        raise ValueError(f"Unsupported driver: {driver_name}")


@pytest.fixture
def selenium(selenium, driver_name, headless):
    """Customize selenium driver window size."""
    if headless:
        selenium.set_window_size(1920, 1080)
        selenium.set_window_position(0, 0)
    else:
        selenium.maximize_window()

    return selenium


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # test result
    outcome = yield
    rep = outcome.get_result()

    # write to attributes of (item)
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def test_failed_check(request, selenium):
    yield
    if request.node.rep_call.failed:
        # Saving the screenshot
        screenshot_name = request.node.nodeid.replace("::", "_").replace("/", "_") + ".png"
        path = f"screenshots/{screenshot_name}"
        selenium.save_screenshot(path)

