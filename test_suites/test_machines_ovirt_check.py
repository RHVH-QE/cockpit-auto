import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_machines_ovirt_check import MachinesOvirtCheckPage


class TestMachinesOvirtCheck(MachinesOvirtCheckPage):
    """
    :avocado: enable
    :avocado: tags=he_vm
    """

    def test_disable_create_new_vm(self):
        self.disable_create_new_vm()

    def test_overview_info(self):
        self.get_dumpxml_on_host()
        self.open_vm_row()
        for key in self.OVERVIEW_INFO_NAMES:
            value_in_xml = self.get_overview_info_in_xml(key)
            value_in_ui = self.get_overview_info_on_ui(key)
            self.assertEqual(value_in_xml, value_in_ui)

    def test_cpu_memory_usage_info(self):
        self.open_vm_row()
        self.open_usage_subtab()
        self.assertNotEqual(self.get_cpu_usage_on_ui(), "0.0%")
        self.assertNotEqual(self.get_memory_usage_on_ui(), "0.00GiB")

    def test_disks_info(self):
        self.get_dumpxml_on_host()
        self.open_vm_row()
        self.open_disks_subtab()
        disk_list = self.get_disk_list_in_xml()
        disk_count_on_ui = self.get_disk_count_on_ui()
        self.assertEqual(disk_count_on_ui, str(len(disk_list)))
        for disk in disk_list:
            for column in self.DISK_COLUMN_NAMES:
                target = self.get_disk_info_in_xml(disk, 'target')
                value_in_xml = self.get_disk_info_in_xml(disk, column)
                value_in_ui = self.get_disk_info_on_ui(target, column)
                self.assertEqual(value_in_xml, value_in_ui)

    def test_networks_info(self):
        self.get_dumpxml_on_host()
        self.open_vm_row()
        self.open_networks_subtab()
        network_list = self.get_network_list_in_xml()
        for i in range(len(network_list)):
            network = network_list[i]
            for column in self.NETWORK_COLUMN_NAMES:
                value_in_xml = self.get_network_info_in_xml(network, column)
                value_on_ui = self.get_network_info_on_ui(i + 1, column)
                self.assertEqual(value_in_xml, value_on_ui)

    def test_inline_vnc_console(self):
        self.open_vm_row()
        self.open_consoles_subtub()
        if self.check_inline_vnc_console():
            self.assert_frame_available(self.INLINE_CONSOLE_FRAME_NAME)
        else:
            self.assertEqual(self.get_console_type(), self.EXTERNAL_CONSOLE_NAME)

    def test_external_console(self):
        self.open_vm_row()
        self.open_consoles_subtub()
        self.open_external_console_page()
        self.assertEqual(self.get_console_type(), self.EXTERNAL_CONSOLE_NAME)

        viewer_list = self.get_external_console_info_in_xml()

        # self.launch_remote_viewer()
        # self.assertEqual(self.get_external_console_info_in_vv(), self.VV_FILE_ATTR.format(
        #     viewer_list[0]['ip'], viewer_list[0]['port']))
        self.assertEqual(self.get_consoles_manual_address_on_ui(), viewer_list[0]['ip'])
        for viewer in viewer_list:
            self.assertEqual(self.get_consoles_manual_port_on_ui(viewer['type']), viewer['port'])

    def test_external_console_more_info(self):
        self.open_vm_row()
        self.open_consoles_subtub()
        self.open_external_console_page()
        self.toggle_more_info()

    def test_ovirt_info(self):
        self.open_vm_row()
        self.open_ovirt_subtub()
        for key in self.OVIRT_INFO_NAMES:
            value_in_host = self.get_ovirt_info_on_host(key)
            value_in_ui = self.get_ovirt_info_on_ui(key)
            self.assertEqual(value_in_host, value_in_ui)

    def test_heVm_network_change(self):
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Unplug')
        self.click_network1_plug_button()
        self.assertNotEqual(self.get_network1_plug_button_text(), 'Plug')
        self.assertNotEqual(self.get_network1_state_on_ui(), 'down')
        self.assertNotEqual(self.get_network1_state_on_host(), 'down')


    def test_ovirtVm_network_unplug(self):
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Unplug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Plug')
        self.assertEqual(self.get_network1_state_on_ui(), 'down')
        self.assertEqual(self.get_network1_state_on_host(), 'down')

    def test_ovirtVm_network_plug(self):
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Plug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Unplug')
        self.assertEqual(self.get_network1_state_on_ui(), 'up')
        self.assertEqual(self.get_network1_state_on_host(), 'up')

    def test_restart_heVm(self):
        self.open_vm_row()
        self.reboot_he_vm_on_ui()

    def test_force_reboot_heVm(self):
        self.open_vm_row()
        self.force_reboot_he_vm_on_ui()

    def test_shutdown_heVm(self):
        self.open_vm_row()
        self.shutdown_he_vm_on_ui()

    def test_forceoff_heVm(self):
        self.open_vm_row()
        self.forceoff_he_vm_on_ui()

    def test_sendnmi_heVm(self):
        self.open_vm_row()
        self.sendnmi_he_vm_on_ui()

    def test_supend_heVm(self):
        pass
        # self.open_vm_row()
        # self.suspend_he_vm_on_ui()

    def test_restart_ovirtVm(self):
        self.open_vm_row()
        self.reboot_ovirt_vm_on_ui()

    def test_force_reboot_ovirtVm(self):
        self.open_vm_row()
        self.force_reboot_ovirt_vm_on_ui()

    def test_shutdown_ovirtVm(self):
        self.open_vm_row()
        self.shutdown_ovirt_vm_on_ui()

    def test_forceoff_ovirtVm(self):
        self.open_vm_row()
        self.forceoff_ovirt_vm_on_ui()

    def test_sendnmi_ovirtVm(self):
        self.open_vm_row()
        self.sendnmi_ovirt_vm_on_ui()

    def test_supend_ovirtVm(self):
        self.open_vm_row()
        self.suspend_ovirt_vm_on_ui()

    def test_vdsm_conf_in_ui(self):
        self.check_vdsm_conf_in_ui()

    def test_save_vdsm_conf_in_ui(self):
        self.check_save_vdsm_conf_in_ui()

    def test_vdsm_service_link(self):
        self.click_vdsm_service_mgmt()

    def test_reload_vdsm_conf(self):
        self.check_reload_vdsm_conf_in_ui()

    def test_cluster_info(self):
        self.get_dumpxml_on_host()
        self.click(self.CLUSTER_TOPNAV)
        for key in self.CLUSTER_INFO_NAME:
            value_in_host = self.get_cluster_info_in_xml(key)
            value_in_ui = self.get_cluster_info_in_ui(key)
            self.assertEqual(value_in_host, value_in_ui)

    def test_cluster_host_link(self):
        self.click(self.CLUSTER_TOPNAV)
        self.click_cluster_host_link()

    def test_template_info(self):
        self.click(self.TEMPLATES_TOPNAV)
        for key in self.TEMPLATE_INFO_NAME:
            value_in_host = self.get_template_info_on_host(key)
            value_in_ui = self.get_template_info_in_ui(key)
            self.assertEqual(value_in_host, value_in_ui)

    def test_create_vm_by_template(self):
        self.click(self.TEMPLATES_TOPNAV)
        self.create_vm_by_template()

    def test_create_vm_twice(self):
        self.click(self.TEMPLATES_TOPNAV)
        self.check_create_vm_twice()

    def test_vm_migration(self):
        self.open_vm_row()
        self.open_ovirt_subtub()
        self.migrate_vm_to_additional_host()

    def test_host_to_maintenance(self):
        self.host_to_maintenance()
