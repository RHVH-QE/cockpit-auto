import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_ovirt_dashboard import OvirtDashboardPage


class TestOvirtDashboard(OvirtDashboardPage):
    """
    :avocado: enable
    :avocado: tags=ovirt_dashboard
    """

    def test_health(self):
        def check_icons(dict_a):
            for key, value in dict_a.items():
                text, icon = self.gen_text_icon_in_node_health(key, value)
                self.assert_element_visible(icon)
                if not isinstance(value, dict) or len(value) <= 1:
                    continue
                self.click(text)
                value.pop('status')
                check_icons(value)

        node_check = self.nodectl_check_on_host()
        node_status = node_check['status']
        self.assert_element_visible(self.HEALTH_TEXT % node_status)
        self.assert_element_visible(
            self.HELATH_ICON % self.gen_icon_from_status(node_status))
        self.click(self.HEALTH_TEXT % node_status)
        check_icons(node_check)

    def test_layer(self):
        def check_contents(dict_a):
            for key, value in dict_a.items():
                if not isinstance(value, dict):
                    text = self.get_text(self.NODE_INFO_VALUE % key)
                    self.assertEqual(value, text)
                    continue
                self.click(self.NODE_INFO_TEXT % key)
                if key == "layers":
                    for k, v in value.items():
                        text = self.get_text(self.NODE_INFO_LAYER % k)
                        for i in range(len(v)):
                            self.assertIn(v[i], text)
                    continue
                check_contents(value)

        node_info = self.nodectl_info_on_host()
        current_layer_link = self.CURRENT_LAYER_LINK % node_info['current_layer']
        self.assert_element_visible(current_layer_link)
        self.click(current_layer_link)
        check_contents(node_info)

    def test_rollback_unavailable(self):
        node_info = self.nodectl_info_on_host()
        self.click(self.ROLLBACK_BUTTON_ON_HOME)
        rollback_button = self.ROLLBACK_BUTTON_ON_LAYERS_DISABLE % node_info['current_layer']
        self.assert_element_visible(rollback_button)

    def _test_rollback_available(self):
        pass

    def test_network_info_link(self):
        self.click(self.NETWORK_INFO_LINK)
        self.refresh()
        self.switch_to_frame(self.NETWORK_FRAME_NAME)

    def test_system_log_link(self):
        self.click(self.SYSTEM_LOGS_LINK)
        self.refresh()
        self.switch_to_frame(self.SYSTEM_LOGS_FRAME_NAME)

    def test_storage_link(self):
        self.click(self.STORAGE_LINK)
        self.refresh()
        self.switch_to_frame(self.STORAGE_FRAME_NAME)

    def test_ssh_host_key_link(self):
        ssh_key = self.get_ssh_key_on_host()
        self.click(self.SSH_HOST_KEY_LINK)
        text = self.get_text(self.SSH_HOST_KEY_CONTENT)
        self.assertEqual(ssh_key, text.replace('\n', ''))

    def _test_vm_numbers(self):
        pass
