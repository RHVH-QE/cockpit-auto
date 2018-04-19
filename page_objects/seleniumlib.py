import os
import inspect
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException


DEFAULT_EXPLICIT_WAIT = 1
DEFAULT_TRY = 20

visible = EC.visibility_of_element_located
clickable = EC.element_to_be_clickable
invisible = EC.invisibility_of_element_located
frame = EC.frame_to_be_available_and_switch_to_it
text = EC.text_to_be_present_in_element

LOCATOR_MAP = {'CSS_SELECTOR': By.CSS_SELECTOR,
               'ID': By.ID,
               'NAME': By.NAME,
               'XPATH': By.XPATH,
               'LINK_TEXT': By.LINK_TEXT,
               'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
               'TAG_NAME': By.TAG_NAME,
               'CLASS_NAME': By.CLASS_NAME,
               }

SEPERATOR = ":::"


def by(src_str):
    tmp_str = src_str.format(SEPERATOR).split(SEPERATOR)[0].strip()
    return LOCATOR_MAP.get(tmp_str)


def lc(src_str):
    return src_str.format(SEPERATOR).split(SEPERATOR)[-1].strip()


class Browser(object):

    def __init__(self, browser):
        if browser == 'firefox':
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        self.driver.set_window_size(1400, 1200)
        self.driver.set_page_load_timeout(90)

        self._screenshot_path = None

    @property
    def screenshot_path(self):
        return self._screenshot_path

    @screenshot_path.setter
    def screenshot_path(self, val):
        self._screenshot_path = val

    def open_url(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def refresh(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()

    def _wait(self, by, locator, trytimes, cond):
        element = None
        for count in range(0, trytimes):
            try:
                element = WebDriverWait(
                    self.driver, DEFAULT_EXPLICIT_WAIT).until(cond((by, locator)))
                break
            except:
                pass

        if not element:
            # sample screenshot name is: screenshot-test20Login.png
            # it stores super caller method to name via inspection code stack
            screenshot_file = "screenshot-%s.png" % str(
                inspect.stack()[2][3])
            try:
                self.driver.save_screenshot(
                    os.path.join(self.screenshot_path, screenshot_file))
            except Exception as e:
                screenshot_file = "Unable to catch screenshot: {0} ({1})".format(
                    screenshot_file, e)
                pass
            finally:
                raise Exception('ERR: Unable to locate name: %s' %
                                str(locator), screenshot_file)
        return element

    def switch_to_frame(self, frame_name, wait_times=DEFAULT_TRY):
        el = "XPATH{}//iframe[contains(@name,'%s')]" % frame_name
        self._wait(by(el), lc(el), wait_times, cond=frame)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def click(self, el, wait_times=DEFAULT_TRY):
        """
        el - The descriptor of an element, shoule be like "XPATH{}//..", "ID{}id"
        """
        element = self._wait(by(el), lc(el), wait_times, cond=clickable)
        element.click()

    def click_text(self, text, wait_times=DEFAULT_TRY):
        el = "XPATH{}//*[contains(text(), '%s')]" % text
        self.click(el, wait_times)

    def hover_and_click(self, el_hover, el_click, wait_times=DEFAULT_TRY):
        hover_element = self._wait(by(el_hover), lc(
            el_hover), wait_times, cond=visible)
        ActionChains(self.driver).move_to_element(hover_element).perform()
        self.click(el_click, wait_times)

    def input_text(self, el, new_value, clear=True, wait_times=DEFAULT_TRY):
        element = self._wait(by(el), lc(el), wait_times, cond=visible)
        if clear:
            element.clear()
        if not new_value.endswith('\n'):
            element.send_keys(new_value)
        else:
            new_value = new_value[:-1]
            element.send_keys(new_value)
            element.send_keys(Keys.RETURN)

    def get_text(self, el, wait_times=DEFAULT_TRY):
        element = self._wait(by(el), lc(el), wait_times, cond=visible)
        return element.text

    def assert_element_visible(self, el, wait_times=DEFAULT_TRY):
        self._wait(by(el), lc(el), wait_times, cond=visible)
        return True

    def assert_text_visible(self, text, wait_times=DEFAULT_TRY):
        el = "XPATH{}//*[contains(text(), '%s')]" % text
        self.assert_element_visible(el, wait_times)
        
    def assert_text_expected(self, el, text):
        element_text = self.get_text(el)
        if text not in element_text:
            raise Exception("ERR: The expected text is unavailable.")

    def assert_text_not_expected(self, el, text):
        element_text = self.get_text(el)
        if text in element_text:
            raise Exception("ERR: The unexpected text is available.")
    
