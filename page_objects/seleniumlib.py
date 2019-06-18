import os
import inspect
import re
from functools import wraps
from avocado import Test
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from utils.machine import Machine
from utils.caseid import check_case_id


DEFAULT_EXPLICIT_WAIT = 1
DEFAULT_TRY = 20

visible = EC.visibility_of_element_located
clickable = EC.element_to_be_clickable
invisible = EC.invisibility_of_element_located
frame = EC.frame_to_be_available_and_switch_to_it
present = EC.presence_of_element_located
text_in = EC.text_to_be_present_in_element

BY_MAP = {'CSS_SELECTOR': By.CSS_SELECTOR,
          'ID': By.ID,
          'NAME': By.NAME,
          'XPATH': By.XPATH,
          'LINK_TEXT': By.LINK_TEXT,
          'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
          'TAG_NAME': By.TAG_NAME,
          'CLASS_NAME': By.CLASS_NAME,
          }


def locator(el_descriptor):
    for key in BY_MAP:
        pattern = r'^{}#'.format(key)
        if re.match(pattern, el_descriptor):
            by = BY_MAP.get(key)
            path = el_descriptor.lstrip('{}#'.format(key))
            break
    else:
        if re.match(r'^//', el_descriptor):
            by = BY_MAP.get('XPATH')
        else:
            by = BY_MAP.get('CSS_SELECTOR')
        path = el_descriptor
    return (by, path)


def retry(attemps=2):
    """
    Decorator to retry operation when
    StaleElementReferenceException, ElementNotInteractableException occurs.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for count in range(0, attemps):
                try:
                    ret = func(*args, **kwargs)
                    return ret
                except (StaleElementReferenceException, ElementNotInteractableException):
                    continue
                except Exception as e:
                    raise e
            else:
                raise RuntimeError(
                    "Too many retries for {}".format(func.__name__))
        return wrapper
    return decorator


class WaitElementTimeOutError(Exception):
    pass


class WaitResults(object):
    def __init__(self):
        self._succeeded = False
        self._element = ""
        self._screenshot = ""

    @property
    def succeeded(self):
        return self._succeeded

    @succeeded.setter
    def succeeded(self, val):
        self._succeeded = val

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, val):
        self._element = val

    @property
    def screenshot(self):
        return self._screenshot

    @screenshot.setter
    def screenshot(self, val):
        self._screenshot = val


class SeleniumTest(Test):
    """
    :avocado: disable
    """

    def setUp(self):
        # initialize polarion case
        self.case_id = None
        self.case_state = None

        # get params from os.environ
        host_string = os.environ.get('HOST_STRING')
        host_port = os.environ.get('HOST_PORT')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        self.browser = os.environ.get('BROWSER')
        selenium_hub = os.environ.get('HUB')

        # create host object
        self.host = Machine(host_string, username, passwd)

        # create selenium webdriver object
        if not selenium_hub:
            if self.browser == 'firefox':
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Chrome()
        else:
            hub_url = 'http://{}:4444/wd/hub'.format(selenium_hub)
            capabilities = self._get_desired_capabilities()
            self.driver = webdriver.Remote(
                command_executor=hub_url, desired_capabilities=capabilities)

        # initialize webdriver
        self.driver.set_window_size(1200, 1200)
        self.driver.set_page_load_timeout(90)
        self.screenshot_path = self.logdir

        # open target page
        self.open_cockpit(host_string, host_port)
        self.login(username, passwd)
        self.open_page()

    @check_case_id
    def tearDown(self):
        self.driver.quit()

    def _get_desired_capabilities(self):
        if self.browser == 'chrome':
            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities['platform'] = 'LINUX'
        elif self.browser == 'firefox':
            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities['platform'] = 'LINUX'
        elif self.browser == 'edge':
            capabilities = DesiredCapabilities.EDGE.copy()
        elif self.browser == 'ie':
            capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()

        return capabilities

    def open_cockpit(self, host_string, host_port='9090'):
        self.driver.get('http://{0}:{1}'.format(host_string, host_port))
        if self.browser == 'edge':
            self.click("#moreInformationDropdownSpan")
            self.click("#invalidcert_continue")
        if self.browser == 'ie':
            self.click("#overridelink")

    def login(self, username, passwd):
        # login page elements
        login_user_text_input = "#login-user-input"
        login_pass_text_input = "#login-password-input"
        login_button = "#login-button"

        self.input_text(login_user_text_input, username)
        self.input_text(login_pass_text_input, passwd)
        self.click(login_button)

    def logout(self):
        # logout elements:
        navbar_dropdown = "#navbar-dropdown"
        go_logout = "#go-logout"

        self.switch_to_default_content()
        self.click(navbar_dropdown)
        self.click(go_logout)

    def open_page(self):
        pass

    def get_current_url(self):
        return self.driver.current_url

    def refresh(self):
        self.driver.refresh()

    def get_title(self):
        return self.driver.title

    def _wait(self, cond, try_times):
        result = WaitResults()
        for count in range(0, try_times):
            try:
                element = WebDriverWait(
                    self.driver, DEFAULT_EXPLICIT_WAIT).until(cond)
                result.succeeded = True
                result.element = element
                break
            except:
                pass
        else:
            screenshot_file = "screenshot-%s.png" % str(inspect.stack()[2][3])
            try:
                self.driver.save_screenshot(
                    os.path.join(self.screenshot_path, screenshot_file))
            except Exception as e:
                screenshot_file = "Unable to catch screenshot: {0} ({1})".format(
                    screenshot_file, e)
            finally:
                result.screenshot = screenshot_file

        return result

    def wait_present(self, el_descriptor, try_times=DEFAULT_TRY):
        cond = present(locator(el_descriptor))
        ret = self._wait(cond, try_times)
        if not ret.succeeded:
            raise WaitElementTimeOutError("Wait '{}' present timeout.".format(
                el_descriptor), ret.screenshot)
        return ret.element

    def wait_visible(self, el_descriptor, try_times=DEFAULT_TRY):
        cond = visible(locator(el_descriptor))
        ret = self._wait(cond, try_times)
        if not ret.succeeded:
            raise WaitElementTimeOutError("Wait '{}' visible timeout.".format(
                el_descriptor), ret.screenshot)
        return ret.element

    def wait_invisible(self, el_descriptor, try_times=DEFAULT_TRY):
        cond = invisible(locator(el_descriptor))
        ret = self._wait(cond, try_times)
        if not ret.succeeded:
            raise WaitElementTimeOutError("Wait '{}' invisible timeout.".format(
                el_descriptor), ret.screenshot)
        return ret.element

    def wait_clickable(self, el_descriptor, try_times=DEFAULT_TRY):
        cond = clickable(locator(el_descriptor))
        ret = self._wait(cond, try_times)
        if not ret.succeeded:
            raise WaitElementTimeOutError("Wait '{}' clickable timeout.".format(
                el_descriptor), ret.screenshot)
        return ret.element

    def wait_in_text(self, el_descriptor, text, try_times=DEFAULT_TRY):
        cond = text_in(locator(el_descriptor), text)
        ret = self._wait(cond, try_times)
        if not ret.succeeded:
            raise WaitElementTimeOutError("Wait '{}' in '{}' timeout.".format(
                text, el_descriptor), ret.screenshot)

    def switch_to_frame(self, frame_name, try_times=DEFAULT_TRY):
        el_descriptor = "iframe[name*='{}']".format(frame_name)
        cond = frame(locator(el_descriptor))
        ret = self._wait(cond, try_times=try_times)
        if not ret.succeeded:
            raise WaitElementTimeOutError(
                "Wait switch to frame {} timeout.".format(frame_name), ret.screenshot)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    @retry(attemps=2)
    def click(self, el_descriptor, try_times=DEFAULT_TRY):
        element = self.wait_clickable(el_descriptor, try_times)
        element.click()

    def click_text(self, text, try_times=DEFAULT_TRY):
        el_descriptor = "//*[contains(text(), '{}')]".format(text)
        self.click(el_descriptor, try_times)

    def hover_and_click(self, el_hover, el_click=None, try_times=DEFAULT_TRY):
        hover_element = self.wait_visible(el_hover, try_times)
        actions = ActionChains(self.driver)
        actions.move_to_element(hover_element)
        if not el_click:
            # hover and click the same element
            actions.click(hover_element)
            actions.perform()
        else:
            # hover to one element, then click another element
            actions.perform()
            self.click(el_click, try_times)

    @retry(attemps=2)
    def input_text(self, el_descriptor, new_value, clear=True, control=False, try_times=DEFAULT_TRY):
        element = self.wait_visible(el_descriptor, try_times)
        if clear:
            element.clear()
        if control:
            element.send_keys(Keys.CONTROL + 'a')
        if not new_value.endswith('\n'):
            element.send_keys(new_value)
        else:
            new_value = new_value[:-1]
            element.send_keys(new_value)
            element.send_keys(Keys.RETURN)

    @retry(attemps=2)
    def get_text(self, el_descriptor, try_times=DEFAULT_TRY):
        element = self.wait_visible(el_descriptor, try_times)
        return element.text

    @retry(attemps=2)
    def get_attribute(self, el_descriptor, attr_name, try_times=DEFAULT_TRY):
        element = self.wait_present(el_descriptor, try_times)
        return element.get_attribute(attr_name)

    def assert_element_visible(self, el_descriptor, try_times=DEFAULT_TRY):
        try:
            self.wait_visible(el_descriptor, try_times)
        except WaitElementTimeOutError:
            self.fail()

    def assert_element_invisible(self, el_descriptor, try_times=DEFAULT_TRY):
        try:
            self.wait_invisible(el_descriptor, try_times)
        except WaitElementTimeOutError:
            self.fail()

    def assert_in_text(self, el_descriptor, text, try_times=DEFAULT_TRY):
        try:
            self.wait_in_text(el_descriptor, text, try_times)
        except WaitElementTimeOutError:
            self.fail()

    def assert_frame_available(self, frame_name, try_times=DEFAULT_TRY):
        try:
            self.switch_to_frame(frame_name, try_times)
        except WaitElementTimeOutError:
            self.fail()

    def assert_text_visible(self, text, try_times=DEFAULT_TRY):
        el_descriptor = "//*[contains(text(), '{}')]".format(text)
        self.assert_element_visible(el_descriptor, try_times)

    def assert_text_in_element(self, el_descriptor, text, try_times=DEFAULT_TRY):
        element_text = self.get_text(el_descriptor, try_times)
        if text not in element_text:
            self.fail("The expected text '{}' is not in element {}.".format(
                text, el_descriptor))

    def assert_text_not_in_element(self, el_descriptor, text, try_times=DEFAULT_TRY):
        element_text = self.get_text(el_descriptor, try_times)
        if text in element_text:
            self.fail("The unexpected text '{}' is in element {}.".format(
                text, el_descriptor))
