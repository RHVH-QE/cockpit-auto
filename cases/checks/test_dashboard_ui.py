import logging
import re
from pages.dashboard_ui_page import DashboardUiPage
from cases.helpers import CheckBase


log = logging.getLogger('bender')


class TestDashboardUi(CheckBase):

    page = None

    def set_page(self):
        self.page = DashboardUiPage(self._driver)

    def check_node_status(self):
        """
        Purpose:
            Check node status in virtualization dashboard
        """
        log.info('Checking node status in virtualization dashboard...')
        try:
            # Check basic elements
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.error(e)
            return False

        with self.page.switch_to_frame(self.page.frame_right_name):  
            try:
                # Check current layer is correct
                test_layer = self._build + '+1'
                assert self.page.cur_layer_link.text == test_layer, \
                    "Current layer is {}, not {}".format(
                        self.page.cur_layer_link.text, test_layer)

                # Check rollback button
                assert self.page.rollback_btn, "Rollback button not exists"
            except AssertionError as e:
                log.error(e)
                return False

        return True

    def check_vms_quantity(self):
        """
        Purpose:
            Check the running Virtual Machines quantity in virtualization dashboard
        """
        log.info("Check the running Virtual Machines quantity in virtualization dashboard")

        with self.page.switch_to_frame(self.page.frame_right_name):
            # VM quantity is 0 where no vms are running
            try:
                assert re.search('0', self.page.vm_quantity.text), \
                    "VM quantity is not 0"
            except AssertionError as e:
                log.error(e)
                return False
        return True
        # Todo creating vm via rhvmapi

    def check_node_health(self):
        """
        Purpose:
            Check node health in virtualization dashboard
        """
        log.info("Check node health in virtualization dashboard")

        with self.page.switch_to_frame(self.page.frame_right_name):
            # click 'Health link'
            self.page.health_link.click()
            wev = self.page.wait_until_element_visible
            wev(self.page.node_health_dialog_title)

            # expand the node health dialog
            accordion_header_btn_list = list(self.page.health_dialog_btns)
            for i in accordion_header_btn_list[0:4]:
                i.click()
            self.page.wait(10)
            ok_number = len(list(self.page.ok_icons))
            try:
                assert ok_number == 16, "OK number is {}, not 16".format(ok_number)
            except AssertionError as e:
                log.error(e)
                return False
            finally:
                # Close dialog
                close_btn_list = list(self.page.close_btns)
                for j in close_btn_list[0:]:
                    j.click()

        return True

    def check_node_info(self):
        """
        Purpose:
            Check node information in virtualization dashboard
        """
        log.info("Check node information in virtualization dashboard")

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.cur_layer_link.click()
                wev = self.page.wait_until_element_visible
                wev(self.page.cur_layer_dialog_title)
                self.page.wait(5)

                accordion_header_btn_list = list(self.page.layer_dialog_btns)
                for i in accordion_header_btn_list:
                    i.click()
                self.page.wait(3)

                # Current layer should be identical with build layer
                test_layer = self._build + '+1'
                entry_txt_list = list(self.page.entry_txts)
                assert entry_txt_list[1].text == test_layer, \
                    "Test layer fail"

                # Since no update action on the new fresh installed
                # system, default layer is current layer
                assert entry_txt_list[0].text == entry_txt_list[1].text, \
                    "Default is not current layer"

                # Todo: check other info like kernel, initrd, etc

                close_btn_list = list(self.page.close_btns)
                for j in close_btn_list[0:]:
                    j.click()
        except AssertionError as e:
            log.error(e)
            return False
        return True

    def check_network_page(self):
        """
        Purpose:
            Go to the Networking page in virtualization dashboard
        """
        log.info("Go to the Networking page in virtualization dashboard")

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.network_info_link.click()
                self.page.wait(3)
                assert re.search('network', self.page.w.current_url), \
                    "Not directed to network page"
        except AssertionError as e:
            log.error(e)
            return False
        return True

    def check_logs_page(self):
        """
        Purpose:
            Go to the Logs page in virtualization dashboard
        """
        log.info("Go to the Logs page in virtualization dashboard")

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.system_logs_link.click()
                self.page.wait(3)
                assert re.search('systems/logs', self.page.w.current_url), \
                    "Not directed to system logs page"
        except AssertionError as e:
            log.error(e)
            return False
        return True

    def check_storage_page(self):
        """
        Purpose:
            Go to the Storage page in virtualization dashboard
        """
        log.info("Go to the Storage page in virtualization dashboard")

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.storage_link.click()
                self.page.wait(3)
                assert re.search('storage', self.page.w.current_url), \
                    "Not directed to storage page"
        except AssertionError as e:
            log.error(e)
            return False
        return True

    def check_ssh_key(self):
        """
        Purpose:
            Check the ssh host key in virtualization dashboard
        """
        log.info("Check the ssh host key in virtualization dashboard")

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.ssh_key_link.click()
                self.page.wait(3)
                assert self.page.ssh_key_dialog_title, \
                    "SSH key error"
        except AssertionError as e:
            log.error(e)
            return False
        return True
