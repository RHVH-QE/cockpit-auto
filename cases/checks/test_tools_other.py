import logging
import os
import re
from selenium import webdriver
from pages.tools_account_page import AccountPage
from pages.tools_diagnostic_page import DiagnosticPage
from pages.tools_selinux_page import SelinuxPage
from pages.tools_kdump_page import KdumpPage
from pages.kdump_service_page import KdumpServicePage
from cases.helpers import CheckBase


log = logging.getLogger('bender')


class TestToolsOther(CheckBase):

    page = None
    test_history = []

    def init_browser(self):
        if self.browser == 'firefox':
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.dir', '/tmp')
            driver = webdriver.Firefox(firefox_profile=profile)
            driver.implicitly_wait(20)
            driver.root_uri = "https://{}:9090".format(self.host_string)
        elif self.browser == 'chrome':
            options = webdriver.ChromeOptions()
            prefs = {'download.default_directory': '/tmp'}
            options.add_experimental_option('prefs', prefs)
            driver = webdriver.Chrome(chrome_options=options)
            driver.implicitly_wait(20)
            driver.root_uri = "https://{}:9090".format(self.host_string)
        else:
            raise NotImplementedError
        driver.maximize_window()
        self._driver = driver

    def _clean_account(self, username):
        cmd = "id {}".format(username)
        ret = self.run_cmd(cmd)
        if ret[0]:
            cmd = "userdel {}".format(username)
            self.run_cmd(cmd)

    def _check_account_created(self, username):
        cmd = "id {}".format(username)
        ret = self.run_cmd(cmd)
        assert ret[0], "{} not exists".format(username)

    def _user_create_from_account_page(self, fullname, username, passwd):
        with self.page.switch_to_frame(self.page.frame_right_name):
            log.info("Click AccountPage.accounts_create_btn")
            self.page.accounts_create_btn.click()
            self.page.wait(1)

            log.info("Input AccountPage.real_name_input with %s", fullname) 
            self.page.real_name_input.clear()
            self.page.wait(1)
            self.page.real_name_input.send_keys(fullname)
            self.page.wait(3)

            log.info("Input AccountPage.user_name_input with %s", username)
            self.page.user_name_input.clear()
            self.page.wait(1)
            self.page.user_name_input.send_keys(username)
            self.page.wait(3)

            log.info("Input AccountPage.password_input with %s", passwd)
            self.page.password_input.clear()
            self.page.wait(1)
            self.page.password_input.send_keys(passwd)
            self.page.wait(3)

            self.page.confirm_input.clear()
            self.page.wait(1)
            self.page.confirm_input.send_keys(passwd)
            self.page.wait(3)

            log.info("Click AccountPage.create_btn")
            self.page.create_btn.click()
            self.page.wait(3)

    def check_new_account(self):
        """
        Purpose:
            Create account in cockpit
        """
        log.info('Checking create account in cockpit...')
        self.page = AccountPage(self._driver)
        self.test_history.append("check_new_account")

        log.info("Checking basic elements")
        try:
            # Check basic elements
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.exception(e)
            return False

        fullname = self._config['fullname']
        username = self._config['username']
        passwd = self._config['password']

        log.info("Clean cockpit account if existing")
        self._clean_account(username)

        try:
            self._user_create_from_account_page(fullname, username, passwd)
            self._check_account_created(username)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def _clean_sosreport(self):
        cmd = "rm -f /tmp/sosreport-*.xz"
        self.local_cmd(cmd)  

    def _check_sosreport_downloaded(self):
        cmd = "test -f /tmp/sosreport-*.xz"
        ret = self.local_cmd(cmd)
        if not ret[0]:
            return False
        return True

    def check_create_diagnostic(self):
        """
        Purpose:
            Create diagnositc report
        """
        log.info("Checking create diagnostic report")
        self.page = DiagnosticPage(self._driver)
        self.test_history.append("check_create_diagnostic")

        log.info("Basic elements check")
        try:
            # Check basic elements
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.exception(e)
            return False

        self._clean_sosreport()

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                log.info("Click AccountPage.create_report_btn")
                self.page.create_report_btn.click()
                self.page.wait_until_element_visible(
                    self.page.download_sos_btn, timeout=300)

                self.page.download_sos_btn.click()
                self.page.wait(30)
        except Exception as e:
            log.exception(e)
            return False

        return self._check_sosreport_downloaded()

    def _check_policy(self, expected="Enforcing"):
        cmd = "getenforce"
        ret = self.run_cmd(cmd)
        return ret[1] == expected

    def check_selinux_policy(self):
        """
        Purpose:
            Check SELinux enforce policy status
        """
        log.info("Check SELinux enforce policy status")
        self.page = SelinuxPage(self._driver)
        self.test_history.append("check_selinux_policy")

        try:
            # Check basic elements
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.exception(e)
            return False

        if not self._check_policy(expected="Enforcing"):
            log.exception("Fresh installed selinux policy is not Enforcing")
            return False

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.policy_btn.click()
                self.page.wait(3)

                assert self._check_policy(expected="Permissive"), \
                    "SElinux policy not changed to Permissive via button"

                self.page.policy_btn.click()
                self.page.wait(3)
                assert self._check_policy(expected="Enforcing"), \
                    "SElinux policy not changed to Enforcing via button"
        except Exception as e:
            log.exception(e)
            return False
        return True

    def _stop_kdump_from_service_page(self):
        self.page.service_status_select.click()
        self.page.wait(1)
        self.page.stop_btn.click()
        self.page.wait(1)

        cmd = "systemctl status kdump.service|grep Active"
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False
        output = ret[1]
        status = output.split()[1].strip()
        assert status == "inactive", \
            "Failed to stop the kdump service, as status is {}".format(status)

    def _start_kdump_from_service_page(self):
        self.page.service_status_select.click()
        self.page.wait(1)
        self.page.start_btn.click()
        self.page.wait(1)

        cmd = "systemctl status kdump.service|grep Active"
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False
        output = ret[1]
        status = output.split()[1].strip()
        assert status == "active", \
            "Failed to start the kdump service, as status is {}".format(status)

    def _disable_kdump_from_service_page(self):
        self.page.enable_disable_select.click()
        self.page.wait(1)
        self.page.disable_btn.click()
        self.page.wait(1)

        cmd = "systemctl status kdump.service|grep Loaded"
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False
        output = ret[1]
        status = output.split(';')[1].strip()
        assert status == "disabled", \
            "Failed to disable the kdump service, as status is {}".format(status)

    def _enable_kdump_from_service_page(self):
        self.page.enable_disable_select.click()
        self.page.wait(1)
        self.page.enable_btn.click()
        self.page.wait(1)

        cmd = "systemctl status kdump.service|grep Loaded"
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False
        output = ret[1]
        status = output.split(';')[1].strip()
        assert status == "enabled", \
            "Failed to enable the kdump service, as status is {}".format(status)

    def check_kdump_service(self):
        """
        Purpose:
            Check the kdump service in cockpit
        """
        log.info("Check the kdump service in cockpit")
        self.page = KdumpPage(self._driver)

        self.test_history.append("check_kdump_service")

        try:
            # Check basic elements
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.exception(e)
            return False

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.service_link.click()
                self.page.wait(3)
                assert re.search(
                    'system/services#/kdump.service', self.page.current_url), \
                    "Not direct to kdump service page"
        except Exception as e:
            log.exception(e)
            return False

        self.page = KdumpServicePage(self._driver)

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self._stop_kdump_from_service_page()
                self._start_kdump_from_service_page()
                self._disable_kdump_from_service_page()
                self._enable_kdump_from_service_page()
        except Exception as e:
            log.exception(e)
            return False
        return True

    def _clean_vmcore(self):
        cmd = "find /var/crash -type f -name vmcore"
        ret = self.run_cmd(cmd, timeout=3600)
        vmcores = ret[1].split()
        for vmcore in vmcores:
            each_dir = os.path.dirname(vmcore)
            cmd = "rm -rf {}".format(each_dir)
            self.run_cmd(cmd)

    def _check_vmcore_created(self):
        cmd = "find /var/crash -type f -name vmcore"
        ret = self.run_cmd(cmd, timeout=3600)
        if not ret[0]:
            return False
        return ret[1]

    def _create_local_dump_from_kdump_page(self):
        with self.page.switch_to_frame(self.page.frame_right_name):
            log.info("Click KdumpPage.dump_location_link")
            self.page.dump_location_link.click()
            self.page.wait(1)
            
            log.info("Click KdumpPage.compression_checkbox")
            self.page.compression_checkbox.click()
            self.page.wait_until_element_visible(
                self.page.test_config_btn, timeout=300)

            log.info("Click KdumpPage.test_config_btn")
            self.page.test_config_btn.click()
            self.page.wait(3)
            
            log.info("Click KdumpPage.crash_system_btn")
            self.page.crash_system_btn.click()

    def check_vmcore_local(self):
        """
        Purpose:
            Capture vmcore at local via kdump function in cockpit
        """
        log.info("Capture vmcore at local via kdump function in cockpit")
        self.page = KdumpPage(self._driver)
        self.test_history.append("check_vmcore_local")

        try:
            # Check basic elements
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.exception(e)
            return False
        
        self._clean_vmcore()

        try:
            self._create_local_dump_from_kdump_page()
            if not self._check_vmcore_created():
                raise Exception("Vmcore not created")
        except Exception as e:
            log.exception(e)
            return False
        return True

    def teardown(self):
        log.info("Tear down work...")
        log.info("Close the browser")
        self.close_browser()

        if "check_new_account" in self.test_history:
            log.info("Clean the account if created")
            username = self._config['username']
            self._clean_account(username)
        if "check_create_diagnostic" in self.test_history:
            log.info("Clean the sosreport if downloaded")
            self._clean_sosreport()
        if "check_vmcore_local" in self.test_history:
            log.info("Clean the vmcore if generated")
            self._clean_vmcore()
