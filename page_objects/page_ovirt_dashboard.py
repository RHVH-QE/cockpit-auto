import simplejson
import time
from seleniumlib import SeleniumTest


class OvirtDashboardPage(SeleniumTest):
    """
    :avocado: disable
    """

    OVIRT_DASHBOARD_FRAME_NAME = "/ovirt-dashboard"
    DASHBOARD_LINK = "a[href='#/dashboard']"

    OK_ICON = "pficon-ok"
    WARN_ICON = "pficon-warning-triangle-o"

    # Node Health
    HEALTH_TEXT = "tbody:nth-child(2) tr:nth-child(1) td:nth-child(2) a div"
    HEALTH_ICON = HEALTH_TEXT + " span"

    NODE_HEALTH_ICON = "//*[text()='%s']//following-sibling::*//*[contains(@class, 'pficon')]"

    # Node layer
    CURRENT_LAYER_LINK = "tbody:nth-child(2) tr:nth-child(2) td:nth-child(2) a"

    # Node information
    NODE_INFO_ITEM = "//*[@class='accordion-header' and text()='%s']"
    NODE_INFO_ARG = "//strong[contains(text(), '%s')]//parent::*//following-sibling::*"
    NODE_INFO_LAYER = "//*[text()='%s']//following-sibling::*"

    # Rollback button
    ROLLBACK_BUTTON_ON_HOME = "tbody:nth-child(2) tr:nth-child(2) td:nth-child(2) button"
    ROLLBACK_BUTTON_ON_LAYERS = "//*[text()='Available Layers']//parent::*//following-sibling::*" \
        "//*[text()='%s']//following-sibling::*/button[text()='Rollback']"
    ROLLBACK_ALERT = "//*[contains(@class, 'alert') and contains(text(), '%s')]"

    # System
    NETWORK_INFO_LINK = "tbody:nth-child(4) tr:nth-child(1) a"
    SYSTEM_LOGS_LINK = "tbody:nth-child(4) tr:nth-child(2) a"
    STORAGE_LINK = "tbody:nth-child(4) tr:nth-child(3) a"
    SSH_HOST_KEY_LINK = "tbody:nth-child(5) a"
    SSH_HOST_KEY_CONTENT = "tbody:nth-child(5) .modal-body div"

    def open_page(self):
        self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)
        self.click(self.DASHBOARD_LINK)

    def get_health_text(self):
        return self.get_text(self.HEALTH_TEXT)

    def get_health_icon(self):
        return self.get_attribute(self.HEALTH_ICON, "class")

    def open_node_health_window(self):
        self.click(self.HEALTH_TEXT)

    def open_item_on_node_health(self, item_name):
        self.click(self.NODE_HEALTH_ICON % item_name)

    def get_item_icon_on_node_health(self, item_name):
        return self.get_attribute(self.NODE_HEALTH_ICON % item_name, "class")

    def get_current_layer_text(self):
        return self.get_text(self.CURRENT_LAYER_LINK)

    def open_node_information_window(self):
        self.click(self.CURRENT_LAYER_LINK)

    def toggle_item_on_node_info(self, item_name):
        self.click(self.NODE_INFO_ITEM % item_name)

    def get_arg_value_on_node_info(self, arg_name):
        return self.get_text(self.NODE_INFO_ARG % arg_name)

    def get_layer_on_node_info(self, layer_name):
        return self.get_text(self.NODE_INFO_LAYER % layer_name)

    def open_rollback_window(self):
        self.click(self.ROLLBACK_BUTTON_ON_HOME)

    def get_rollback_attr_on_layer(self, layer_name):
        return self.get_attribute(self.ROLLBACK_BUTTON_ON_LAYERS % layer_name, 'class')

    def open_network_info_link(self):
        self.click(self.NETWORK_INFO_LINK)
        self.refresh()

    def open_system_logs_link(self):
        self.click(self.SYSTEM_LOGS_LINK)
        self.refresh()

    def open_storage_link(self):
        self.click(self.STORAGE_LINK)
        self.refresh()

    def get_ssh_key_on_page(self):
        self.click(self.SSH_HOST_KEY_LINK)
        return self.get_text(self.SSH_HOST_KEY_CONTENT).replace('\n', '')

    def execute_rollback_on_layer(self, layer_name):
        self.click(self.ROLLBACK_BUTTON_ON_LAYERS % layer_name)

    def nodectl_check_on_host(self):
        cmd = 'nodectl check --machine-readable'
        ret = self.host.execute(cmd)
        return simplejson.loads(ret)

    def nodectl_info_on_host(self):
        cmd = 'nodectl info --machine-readable'
        ret = self.host.execute(cmd)
        return simplejson.loads(ret)

    def get_ssh_key_on_host(self):
        cmd = "cat /etc/ssh/ssh_host_rsa_key | tr -d '\r\n'"
        return self.host.execute(cmd)

    def gen_icon_from_status(self, status):
        if status == 'ok':
            return self.OK_ICON
        else:
            return self.WARN_ICON

    def gen_expected_name_from_nodectl_check(self, nodectl_check_key):
        if nodectl_check_key != "vdsmd":
            name = nodectl_check_key.capitalize().replace("_", " ")
        else:
            name = nodectl_check_key
        return name

    def gen_expected_icon_from_nodectl_check(self, nodectl_check_value):
        if not isinstance(nodectl_check_value, dict):
            status = nodectl_check_value
        else:
            status = nodectl_check_value["status"]
        return self.gen_icon_from_status(status)
