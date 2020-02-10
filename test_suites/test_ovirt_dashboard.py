import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_ovirt_dashboard import OvirtDashboardPage
from utils.caseid import add_case_id


class TestOvirtDashboard(OvirtDashboardPage):
    """
    :avocado: enable
    :avocado: tags=ovirt_dashboard
    """

    @add_case_id("RHEVM-23307")
    def test_node_vm_quantity(self):
        """
        :avocado: tags=dashboard_tier1
        """
        self.check_vm_quantity()

    @add_case_id("RHEVM-23308")
    def test_node_status(self):
        """
        :avocado: tags=dashboard_tier1
        """
        self.check_function_domains()
        self.check_node_status_items()

    @add_case_id("RHEVM-23309")
    def test_node_health(self):
        """
        :avocado: tags=dashboard_tier1
        """
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


    @add_case_id("RHEVM-23317")
    def test_network_info_link(self):
        """
        :avocado: tags=dashboard_tier2
        """
        self.open_network_info_link()
        self.assertIn('Networking', self.get_title())

    @add_case_id("RHEVM-23318")
    def test_system_log_link(self):
        """
        :avocado: tags=dashboard_tier2
        """
        self.open_system_logs_link()
        self.assertIn('Logs', self.get_title())

    @add_case_id("RHEVM-23319")
    def test_storage_link(self):
        """
        :avocado: tags=dashboard_tier2
        """
        self.open_storage_link()
        self.assertIn('Storage', self.get_title())

    @add_case_id("RHEVM-23320")
    def test_ssh_host_key_link(self):
        """
        :avocado: tags=dashboard_tier2
        """
        ssh_key_on_host = self.get_ssh_key_on_host()
        ssh_key_on_ui = self.get_ssh_key_on_page()
        self.assertEqual(ssh_key_on_host, ssh_key_on_ui)

    @add_case_id("RHEVM-23311")
    def test_node_information(self):
        """
        :avocado: tags=dashboard_tier2
        """
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

    @add_case_id("RHEVM-23313")
    def test_rollback(self):
        """
        :avocado: tags=dashboard_tier2
        """
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