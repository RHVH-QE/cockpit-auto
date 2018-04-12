import os
import time
from avocado import Test
from machinelib import Machine
from seleniumlib import Browser


class PageTest(Test):
    """
    :avocado: disable
    """

    def setUp(self):
        host_string = os.environ['HOST_STRING']
        username = os.environ['USERNAME']
        passwd = os.environ['PASSWD']
        browser = os.environ['BROWSER']

        self.machine = Machine(host_string, username, passwd)

        self.browser = Browser(browser)
        self.browser.screenshot_path = self.logdir
        self.browser.open_url('http://%s:9090' % host_string)
        self.login(username, passwd)
        self.open_page()

    def tearDown(self):
        self.browser.close()

    def login(self, username, passwd):
        # login page elements
        login_user_text_input = "ID{}login-user-input"
        login_pass_text_input = "ID{}login-password-input"
        login_button = "ID{}login-button"

        self.browser.input_text(login_user_text_input, username)
        self.browser.input_text(login_pass_text_input, passwd)
        self.browser.click(login_button)

    def logout(self):
        # logout elements:
        navbar_dropdown = "ID{}navbar-dropdown"
        go_logout = "ID{}go-logout"

        self.browser.switch_to_default_content()
        self.browser.click(navbar_dropdown)
        self.browser.click(go_logout)

    def open_page(self):
        pass
