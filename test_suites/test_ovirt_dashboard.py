import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_ovirt_dashboard import OvirtDashboardPage


class TestOvirtDashboard(OvirtDashboardPage):
    """
    :avocado: enable
    :avocado: tags=ovirt_dashboard
    """

    def test_health_status(self):
        nodectl_check = self.nodectl_check_on_host()
        expected_status = nodectl_check['status']
        expected_icon = self.gen_icon_from_status(expected_status)
        status_on_ui = self.get_health_text()
        icon_on_ui = self.get_health_icon()
        self.assertEqual(status_on_ui, expected_status)
        self.assertIn(status_on_ui, icon_on_ui)

    def test_node_health(self):
        def check_icons(dict_a):
            for key, value in dict_a.items():
                expected_name = self.gen_expected_name_from_nodectl_check(key)
                expected_icon = self.gen_expected_icon_from_nodectl_check(
                    value)
                icon_on_ui = self.get_item_icon_on_node_health(
                    expected_name)
                self.assertIn(expected_icon, icon_on_ui)
                if not isinstance(value, dict) or len(value) <= 1:
                    continue
                self.open_item_on_node_health(expected_name)
                value.pop('status')
                check_icons(value)

        nodectl_check = self.nodectl_check_on_host()
        self.open_node_health_window()
        check_icons(nodectl_check)

    def test_current_layer(self):
        nodectl_info = self.nodectl_info_on_host()
        expected_current_layer = nodectl_info['current_layer']
        current_layer_on_ui = self.get_current_layer_text()
        self.assertEqual(expected_current_layer, current_layer_on_ui)

    def test_node_information(self):
        global mem
        mem = None

        def check_contents(dict_a):
            global mem
            for key, value in dict_a.items():
                if not isinstance(value, dict):
                    text = self.get_arg_value_on_node_info(key)
                    self.assertEqual(value, text)
                    continue
                if 'rhvh' in key:
                    if mem:
                        self.toggle_item_on_node_info(mem)
                    mem = key
                self.toggle_item_on_node_info(key)
                if key == "layers":
                    for k, v in value.items():
                        text = self.get_layer_on_node_info(k)
                        self.assertIn(v[0], text)
                    continue
                check_contents(value)

        nodectl_info = self.nodectl_info_on_host()
        self.open_node_information_window()
        check_contents(nodectl_info)

    def test_rollback(self):
        nodectl_info = self.nodectl_info_on_host()
        current_layer = nodectl_info['current_layer']
        layers = nodectl_info['layers'].values()
        available_layer = None
        self.open_rollback_window()
        for layer in layers:
            rollback_attr = self.get_rollback_attr_on_layer(layer[0])
            if layer[0] != current_layer:
                self.assertNotIn('disabled', rollback_attr)
                available_layer = layer[0]
            else:
                self.assertIn('disabled', rollback_attr)
        if available_layer:
            self.execute_rollback_on_layer(available_layer)
            self.assert_element_visible(self.ROLLBACK_ALERT % available_layer)

    def test_network_info_link(self):
        self.open_network_info_link()
        self.assertIn('Networking', self.get_title())

    def test_system_log_link(self):
        self.open_system_logs_link()
        self.assertIn('Logs', self.get_title())

    def test_storage_link(self):
        self.open_storage_link()
        self.assertIn('Storage', self.get_title())

    def test_ssh_host_key_link(self):
        ssh_key_on_host = self.get_ssh_key_on_host()
        ssh_key_on_ui = self.get_ssh_key_on_page()
        self.assertEqual(ssh_key_on_host, ssh_key_on_ui)
