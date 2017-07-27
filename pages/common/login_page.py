import re
from utils.page_objects import PageObject, PageElement
from fabric.api import run, settings


class LoginPage(PageObject):
    """Login page action method come here"""

    brand_log = PageElement(id_="brand")

    username_input = PageElement(id_="login-user-input")
    password_input = PageElement(id_="login-password-input")
    login_btn = PageElement(id_="login-button")
    login_error_message = PageElement(id_="login-error-message")

    # Other options
    other_option = PageElement(id_="option-caret")
    server_input = PageElement(id_="server-field")

    # After click the Login button
    md5_input = PageElement(id_="conversation-input")

    def __init__(self, *args, **kwargs):
        super(LoginPage, self).__init__(*args, **kwargs)
        self.get("/")
        self.wait_until_element_visible(self.username_input)

    def basic_check_elements_exists(self):
        assert self.username_input, "input username not exist"
        assert self.password_input, "input password not exist"
        assert self.login_btn, "login btn not exist"
        self.wait()

    def login_with_credential(self, username, password):
        self.username_input.clear()
        self.wait(0.5)
        self.username_input.send_keys(username)
        self.wait(0.5)

        self.password_input.clear()
        self.wait(0.5)
        self.password_input.send_keys(password)
        self.wait(0.5)

        self.login_btn.click()
        self.wait()

    def login_with_incorrect_credential(self):
        self.username_input.send_keys("cockpit")
        self.password_input.send_keys("none")
        self.login_btn.click()
        self.wait(5)

        assert re.search(
            "Wrong user name or password",
            self.login_error_message.text),    \
            "No error message prompt with incorrect credential login"

    def check_allow_unknown_default(self):
        """
        Purpose:
            Login into remote machine with "allowUnknow" is default in cockpit
        """
        with settings(warn_only=True):
            cmd = "rm -f /etc/cockpit/cockpit.conf"
            run(cmd)
            cmd = "service cockpit restart"
            run(cmd)
        self.username_input.send_keys("root")
        self.password_input.send_keys("redhat")

        self.other_option.click()
        self.server_input.send_keys("10.66.8.173")
        self.login_btn.click()
        self.wait(5)

        assert re.search(
            "Refusing to connect. Host is unknown",
            self.login_error_message.text),     \
            "Wrong error message [%s] prompt with allownUnknow default" % \
            self.login_error_message.text

    def check_allow_unknown_true(self, another_ip, another_user,
                                 another_password):
        """
        Purpose:
            Login into remote machine with "allowUnknow" is true in cockpit
        """
        # Modify "allowUnknown=True" in /etc/cockpit/cockpit.conf
        source = '''
[SSH-Login]
host=%s
allowUnknown=true
'''
        with settings(warn_only=True):
            cmd = "rm -f /etc/cockpit/cockpit.conf"
            run(cmd)
            cmd = "echo '%s' >> /etc/cockpit/cockpit.conf" % (
                source % another_ip)
            run(cmd)
            cmd = "service cockpit restart"
            run(cmd)
        self.username_input.send_keys(another_user)
        self.password_input.send_keys(another_password)

        self.other_option.click()
        self.server_input.send_keys(another_ip)
        self.login_btn.click()
        self.wait(5)
        self.login_btn.click()

    def check_allow_unknown_true_wrong_account(self, another_ip):
        """
        Purpose:
            Login into remote machine with "allowUnknow" is true in cockpit
        """
        # Modify "allowUnknown=True" in /etc/cockpit/cockpit.conf
        source = '''
[SSH-Login]
host=%s
allowUnknown=true
''' % another_ip
        with settings(warn_only=True):
            cmd = "rm -f /etc/cockpit/cockpit.conf"
            run(cmd)
            cmd = "echo '%s' >> /etc/cockpit/cockpit.conf" % source
            run(cmd)
            cmd = "service cockpit restart"
            run(cmd)
        self.username_input.send_keys("cockpit")
        self.password_input.send_keys("none")

        self.other_option.click()
        self.server_input.send_keys(another_ip)
        self.login_btn.click()
        self.wait(5)

        assert re.search(
            "Wrong user name or password",
            self.login_error_message.text),     \
            "Wrong error message [%s] prompt with allownUnknow true with wrong account" % \
            self.login_error_message.text

    def check_allow_unknown_true_remote_closed(self, another_ip, another_user,
                                               another_password):
        """
        Purpose:
            Login remote closed host with "allowUnknow" is true in cockpit
        """
        # Modify "allowUnknown=True" in /etc/cockpit/cockpit.conf
        source = '''
[SSH-Login]
host=%s
allowUnknown=true
''' % another_ip
        with settings(warn_only=True):
            cmd = "rm -f /etc/cockpit/cockpit.conf"
            run(cmd)
            cmd = "echo '%s' >> /etc/cockpit/cockpit.conf" % source
            run(cmd)
            cmd = "service cockpit restart"
            run(cmd)
        self.username_input.send_keys(another_user)
        self.password_input.send_keys(another_password)

        self.other_option.click()
        self.server_input.send_keys(another_ip)
        self.login_btn.click()
        self.wait(5)

        assert re.search(
            "Authentication Failed, Server closed connection",
            self.login_error_message.text),     \
            "Wrong error message [%s] prompt with allownUnknow true with remote closed" % \
            self.login_error_message.text

    def check_allow_unknown_true_wrong_address(self):
        """
        Purpose:
            Login remote host with wrong address in cockpit
        """
        # Modify "allowUnknown=True" in /etc/cockpit/cockpit.conf
        source = '''
[SSH-Login]
host=10.8.8.8
allowUnknown=true
'''
        with settings(warn_only=True):
            cmd = "rm -f /etc/cockpit/cockpit.conf"
            run(cmd)
            cmd = "echo '%s' >> /etc/cockpit/cockpit.conf" % source
            run(cmd)
            cmd = "service cockpit restart"
            run(cmd)
        self.username_input.send_keys("root")
        self.password_input.send_keys("redhat")

        self.other_option.click()
        self.server_input.send_keys("10.8.8.8")
        self.login_btn.click()
        self.wait(30)

        assert re.search(
            "Unable to connect to that address",
            self.login_error_message.text),     \
            "Wrong error message [%s] prompt with allownUnknow true with wrong address" % \
            self.login_error_message.text

    def check_allow_unknown_true_empty_username(self, another_ip, another_user,
                                                another_password):
        """
        Purpose:
            Login remote host with empty username in cockpit
        """
        # Modify "allowUnknown=True" in /etc/cockpit/cockpit.conf
        source = '''
[SSH-Login]
host=%s
allowUnknown=true
''' % another_ip
        with settings(warn_only=True):
            cmd = "rm -f /etc/cockpit/cockpit.conf"
            run(cmd)
            cmd = "echo '%s' >> /etc/cockpit/cockpit.conf" % source
            run(cmd)
            cmd = "service cockpit restart"
            run(cmd)

        self.password_input.send_keys(another_password)

        self.other_option.click()
        self.server_input.send_keys(another_ip)
        self.login_btn.click()
        self.wait(5)

        assert re.search(
            "User name cannot be empty",
            self.login_error_message.text),     \
            "Wrong error message [%s] prompt with allownUnknow true with empty user" % \
            self.login_error_message.text
