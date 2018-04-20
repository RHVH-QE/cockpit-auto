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

BY_MAP = {'CSS_SELECTOR': By.CSS_SELECTOR,
          'ID': By.ID,
          'NAME': By.NAME,
          'XPATH': By.XPATH,
          'LINK_TEXT': By.LINK_TEXT,
          'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT,
          'TAG_NAME': By.TAG_NAME,
          'CLASS_NAME': By.CLASS_NAME,
          }

SEPERATOR = ":::"


def locator(el_descriptor):
    el_format = el_descriptor.format(SEPERATOR)
    by = BY_MAP.get(el_format.split(SEPERATOR)[0].strip())
    path = el_format.split(SEPERATOR)[-1].strip()
    return (by, path)


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
        self.driver.quit()

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
                raise Exception('ERR: Unable to locate %s' %
                                str(el_descriptor), screenshot_file)
        return element

    def switch_to_frame(self, frame_name, try_times=DEFAULT_TRY):
        el_descriptor = "XPATH{}//iframe[contains(@name,'%s')]" % frame_name
        self._wait(el_descriptor, cond=frame, try_times=try_times)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def click(self, el_descriptor, try_times=DEFAULT_TRY):
        element = self._wait(
            el_descriptor, cond=clickable, try_times=try_times)
        element.click()

    def click_text(self, text, try_times=DEFAULT_TRY):
        el_descriptor = "XPATH{}//*[contains(text(), '%s')]" % text
        self.click(el_descriptor, try_times)

    def hover_and_click(self, el_hover, el_click, try_times=DEFAULT_TRY):
        hover_element = self._wait(el_hover, cond=visible, try_times=try_times)
        ActionChains(self.driver).move_to_element(hover_element).perform()
        self.click(el_click, try_times)

    def input_text(self, el_descriptor, new_value, clear=True, try_times=DEFAULT_TRY):
        element = self._wait(el_descriptor, cond=visible, try_times=try_times)
        if clear:
            element.clear()
        if not new_value.endswith('\n'):
            element.send_keys(new_value)
        else:
            new_value = new_value[:-1]
            element.send_keys(new_value)
            element.send_keys(Keys.RETURN)

    def get_text(self, el_descriptor, try_times=DEFAULT_TRY):
        element = self._wait(el_descriptor, cond=visible, try_times=try_times)
        return element.text

    def assert_element_visible(self, el_descriptor, try_times=DEFAULT_TRY):
        self._wait(el_descriptor, cond=visible, try_times=try_times)
        return True

    def assert_text_visible(self, text, try_times=DEFAULT_TRY):
        el_descriptor = "XPATH{}//*[contains(text(), '%s')]" % text
        self.assert_element_visible(el_descriptor, try_times)

    def assert_text_in_element(self, el_descriptor, text, try_times=DEFAULT_TRY):
        element_text = self.get_text(el_descriptor, try_times)
        if text not in element_text:
            raise Exception(
                "ERR: The expected text '%s' is not in element %s." % (text, el_descriptor))
        return True

    def assert_text_not_in_element(self, el_descriptor, text, try_times=DEFAULT_TRY):
        element_text = self.get_text(el_descriptor, try_times)
        if text in element_text:
            raise Exception(
                "ERR: The unexpected text '%s' is in element %s." % (text, el_descriptor))
        return True
