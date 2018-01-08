import logging
from pages.tools_account_page import AccountPage
from pages.tools_diagnostic_page import DiagnosticPage
from cases.helpers import CheckBase
from fabric.api import settings, run


log = logging.getLogger('sherry')


class TestToolsOther(CheckBase):

    page = None

    def set_page(self):
        self.page = AccountPage(self._driver)

    def run_cmd(self, cmd, host_string=None, host_user=None, host_pass=None, timeout=60):
        if not host_string:
            host_string = self.host_string
        if not host_user:
            host_user = self.host_user
        if not host_pass:
            host_pass = self.host_pass

        ret = None
        try:
            with settings(
                    host_string=host_string,
                    user=host_user,
                    password=host_pass,
                    disable_known_hosts=True,
                    connection_attempts=60):
                ret = run(cmd, quiet=True, timeout=timeout)
                if ret.succeeded:
                    log.info('Run cmd "%s" succeeded\n"%s"', cmd, ret)
                    return True, ret
                else:
                    log.error('Run cmd "%s" failed\n"%s"', cmd, ret)
                    return False, ret
        except Exception as e:
            log.error('Run cmd "%s" failed with exception "%s"', cmd, e)
            return False, e

    def _check_account_created(self, username, password):
        cmd = "whoami"
        ret = self.run_cmd(cmd, host_user=username, host_pass=password)
        assert ret[0], \
            "Failed to run whoami via new account {}".format(username)
        assert ret[1] == username

    def check_new_account(self):
        """
        Purpose:
            Create account in cockpit
        """
        log.info('Checking create account in cockpit...')
        try:
            # Check basic elements
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.error(e)
            return False
  
        fullname = self._config['fullname']
        username = self._config['username']
        passwd = self._config['password']

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.accounts_create_btn.click()
                self.page.wait(1)
                self.page.real_name_input.clear()
                self.page.wait(1)
                self.page.real_name_input.send_keys(fullname)
                self.page.wait(3)

                self.page.user_name_input.clear()
                self.page.wait(1)
                self.page.user_name_input.send_keys(username)
                self.page.wait(3)

                self.page.password_input.clear()
                self.page.wait(1)
                self.page.password_input.send_keys(passwd)
                self.page.wait(3)

                self.page.confirm_input.clear()
                self.page.wait(1)
                self.page.confirm_input.send_keys(passwd)
                self.page.wait(3)

                self.page.create_btn.click()
                self.page.wait(3)

            self._check_account_created(username, passwd)
        except Exception as e:
            log.exception(e)
            return False

    def check_create_diagnostic(self):
        """
        Purpose:
            Create diagnositc report
        """
        log.info("Checking create diagnostic report")
        self.page = DiagnosticPage(self._driver)

    def teardown(self):
        self.close_browser()
        username = self._config['username']
        cmd = "userdel {}".format(username)
        self.run_cmd(cmd)
