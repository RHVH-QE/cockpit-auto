import os
import inspect
import time
import re
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


DEFAULT_EXPLICIT_WAIT = 1
DEFAULT_TRY = 20

visible = EC.visibility_of_element_located
clickable = EC.element_to_be_clickable
invisible = EC.invisibility_of_element_located
frame = EC.frame_to_be_available_and_switch_to_it

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
        pattern = r'^%s#' % key
        if re.match(pattern, el_descriptor):
            by = BY_MAP.get(key)
            path = el_descriptor.lstrip('%s#' % key)
            break
    else:
        if re.match(r'^//', el_descriptor):
            by = BY_MAP.get('XPATH')
        else:
            by = BY_MAP.get('CSS_SELECTOR')
        path = el_descriptor
    return (by, path)


class NoElementError(Exception):
    pass


class SeleniumTest(Test):
    """
    :avocado: disable
    """

    def setUp(self):
        # get params from os.environ
        host_string = os.environ.get('HOST_STRING')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        browser = os.environ.get('BROWSER')
        selenium_hub = os.environ.get('HUB')

        # create host object
        self.host = Machine(host_string, username, passwd)

        # create selenium webdriver object
        if not selenium_hub:
            if browser == 'firefox':
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Chrome()
        else:
            hub_url = 'http://%s:4444/wd/hub' % selenium_hub
            capabilities = self._get_desired_capabilities(browser)
            self.driver = webdriver.Remote(
                command_executor=hub_url, desired_capabilities=capabilities)

        # initialize webdriver
        self.driver.set_window_size(1200, 1200)
        self.driver.set_page_load_timeout(90)
        self.screenshot_path = self.logdir

        # open target page
        self.open_cockpit(host_string, browser)
        self.login(username, passwd)
        self.open_page()

    def tearDown(self):
        self.driver.quit()

    def _get_desired_capabilities(self, browser):
        if browser == 'chrome':
            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities['platform'] = 'LINUX'
        elif browser == 'firefox':
            capabilities = DesiredCapabilities.FIREFOX.copy()
            capabilities['platform'] = 'LINUX'
        elif browser == 'ie':
            capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()

        return capabilities

    def open_cockpit(self, host_string, browser=None):
        self.driver.get('http://%s:9090' % host_string)
        if browser == 'ie':
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

    def _wait(self, el_descriptor, cond, try_times):
        """
        el_descriptor - The descriptor of an element, shoule be like "XPATH{}//..", "ID{}id"
        """
        element = None
        for count in range(0, try_times):
            try:
                element = WebDriverWait(
                    self.driver, DEFAULT_EXPLICIT_WAIT).until(cond(locator(el_descriptor)))
                break
            except:
                pass

        if not element:
            screenshot_file = "screenshot-%s.png" % str(inspect.stack()[2][3])
            try:
                self.driver.save_screenshot(
                    os.path.join(self.screenshot_path, screenshot_file))
            except Exception as e:
                screenshot_file = "Unable to catch screenshot: {0} ({1})".format(
                    screenshot_file, e)
                pass
            finally:
                raise NoElementError('Unable to locate %s' %
                                     str(el_descriptor), screenshot_file)

        return element

    def switch_to_frame(self, frame_name, try_times=DEFAULT_TRY):
        el_descriptor = "iframe[name*='%s']" % frame_name
        self._wait(el_descriptor, cond=frame, try_times=try_times)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def click(self, el_descriptor, try_times=DEFAULT_TRY):
        element = self._wait(
            el_descriptor, cond=clickable, try_times=try_times)
        try:
            element.click()
        except (StaleElementReferenceException, ElementNotInteractableException):
            element = self._wait(
                el_descriptor, cond=clickable, try_times=try_times)
            element.click()

    def click_text(self, text, try_times=DEFAULT_TRY):
        el_descriptor = "//*[contains(text(), '%s')]" % text
        self.click(el_descriptor, try_times)

    def hover_and_click(self, el_hover, el_click=None, try_times=DEFAULT_TRY):
        hover_element = self._wait(
            el_hover, cond=visible, try_times=try_times)
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

    def input_text(self, el_descriptor, new_value, clear=True, try_times=DEFAULT_TRY):
        element = self._wait(el_descriptor, cond=visible,
                             try_times=try_times)
        if clear:
            element.clear()
        if not new_value.endswith('\n'):
            element.send_keys(new_value)
        else:
            new_value = new_value[:-1]
            element.send_keys(new_value)
            element.send_keys(Keys.RETURN)

    def get_text(self, el_descriptor, try_times=DEFAULT_TRY):
        element = self._wait(el_descriptor, cond=visible,
                             try_times=try_times)
        return element.text

    def get_attribute(self, el_descriptor, attr_name, try_times=DEFAULT_TRY):
        element = self._wait(el_descriptor, cond=visible,
                             try_times=try_times)
        return element.get_attribute(attr_name)

    def assert_element_visible(self, el_descriptor, try_times=DEFAULT_TRY):
        try:
            self._wait(el_descriptor, cond=visible, try_times=try_times)
        except NoElementError:
            self.fail()

    def assert_element_invisible(self, el_descriptor, try_times=DEFAULT_TRY):
        try:
            self._wait(el_descriptor, cond=invisible, try_times=try_times)
        except NoElementError:
            self.fail()

    def assert_text_visible(self, text, try_times=DEFAULT_TRY):
        el_descriptor = "//*[contains(text(), '%s')]" % text
        self.assert_element_visible(el_descriptor, try_times)

    def assert_text_in_element(self, el_descriptor, text, try_times=DEFAULT_TRY):
        element_text = self.get_text(el_descriptor, try_times)
        if text not in element_text:
            self.fail("The expected text '%s' is not in element %s." %
                      (text, el_descriptor))

    def assert_text_not_in_element(self, el_descriptor, text, try_times=DEFAULT_TRY):
        element_text = self.get_text(el_descriptor, try_times)
        if text in element_text:
            self.fail("The unexpected text '%s' is in element %s." %
                      (text, el_descriptor))
