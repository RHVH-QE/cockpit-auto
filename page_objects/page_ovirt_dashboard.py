import simplejson
from page import PageTest


class OvirtDashboardPage(PageTest):
    """
    :avocado: disable
    """

    OVIRT_DASHBOARD_FRAME_NAME = "/ovirt-dashboard"
    DASHBOARD_LINK = "XPATH{}//a[@href='#/dashboard']"

    OK_ICON = "pficon-ok"

    # Node Health
    _HEALTH = "XPATH{}//td[text()='Health']//following-sibling::td"
    HEALTH_TEXT = _HEALTH + "/div[1]//*[contains(text(), '%s')]"
    HELATH_ICON = _HEALTH + "/div[1]//*[contains(@class, '%s')]"

    NODE_HEALTH_TEXT = "XPATH{}//*[text()='%s']"
    NODE_HEALTH_ICON = "//following-sibling::*//*[contains(@class, '%s')]"

    # Node layer
    CURRENT_LAYER_LINK = "LINK_TEXT{}%s"

    # Node information
    NODE_INFO_TEXT = "XPATH{}//*[@class='accordion-header' and text()='%s']"
    NODE_INFO_VALUE = "XPATH{}//strong[contains(text(), '%s')]//parent::*//following-sibling::*"
    NODE_INFO_LAYER = "XPATH{}//*[text()='%s']//following-sibling::*"

    # Rollback button
    ROLLBACK_BUTTON_ON_HOME = "XPATH{}//button[text()='Rollback']"
    ROLLBACK_BUTTON_ON_LAYERS_DISABLE = "XPATH{}//*[text()='Available Layers']//parent::*//following-sibling::*" \
        "//*[text()='%s']//following-sibling::*/button[text()='Rollback' and contains(@class, 'disabled')]"

    # System
    _SYSTEM_INFO_LINK = "XPATH{}//*[contains(text(), '%s')]//following-sibling::*//a[text()='View']"
    NETWORK_INFO_LINK = _SYSTEM_INFO_LINK % 'Networking Information'
    SYSTEM_LOGS_LINK = _SYSTEM_INFO_LINK % 'System Logs'
    STORAGE_LINK = _SYSTEM_INFO_LINK % 'Storage'
    SSH_HOST_KEY_LINK = _SYSTEM_INFO_LINK % 'SSH Host Key'
    SSH_HOST_KEY_CONTENT = "XPATH{}//*[contains(text(), 'BEGIN RSA PRIVATE KEY')]"

    NETWORK_FRAME_NAME = "/network"
    SYSTEM_LOGS_FRAME_NAME = "/system/logs"
    STORAGE_FRAME_NAME = "/storage"

    def open_page(self):
        self.browser.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)
        self.browser.click(self.DASHBOARD_LINK)

    def nodectl_check_on_host(self):
        cmd = 'nodectl check --machine-readable'
        ret = self.host.execute(cmd)
        if not ret[0]:
            raise Exception("ERR: Run `%s` failed on host" % cmd)
        return simplejson.loads(ret[1])

    def nodectl_info_on_host(self):
        cmd = 'nodectl info --machine-readable'
        ret = self.host.execute(cmd)
        if not ret[0]:
            raise Exception("ERR: Run `%s` failed on host" % cmd)
        return simplejson.loads(ret[1])

    def get_ssh_key_on_host(self):
        cmd = "cat /etc/ssh/ssh_host_rsa_key | tr -d '\r\n'"
        ret = self.host.execute(cmd)
        if not ret[0]:
            raise Exception("ERR: Run `%s` failed on host" % cmd)
        return ret[1]

    def gen_icon_from_status(self, status):
        if status == 'ok':
            return self.OK_ICON
        else:
            return "invalid"

    def gen_text_icon_in_node_health(self, node_check_key, node_check_value):
        if node_check_key == "vdsmd":
            text = self.NODE_HEALTH_TEXT % node_check_key
        else:
            text = self.NODE_HEALTH_TEXT % node_check_key.capitalize().replace("_", " ")
        if node_check_key == "status":
            status = node_check_value
        else:
            status = node_check_value["status"]
        icon = text + self.NODE_HEALTH_ICON % self.gen_icon_from_status(status)

        return (text, icon)
