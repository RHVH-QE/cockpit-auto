import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_machines_ovirt_check import MachinesOvirtCheckPage
from utils.caseid import add_case_id


class TestMachinesOvirtCheck(MachinesOvirtCheckPage):
    """
    :avocado: enable
    :avocado: tags=machines_ovirt_check
    """
    @add_case_id("RHEL-118144")
    def test_disable_create_new_vm(self):
        self.disable_create_new_vm()

    @add_case_id("RHEL-113784")
    def test_overview_info(self):
        self.get_dumpxml_on_host()
        self.open_vm_row()
        for key in self.OVERVIEW_INFO_NAMES:
            value_in_xml = self.get_overview_info_in_xml(key)
            value_in_ui = self.get_overview_info_on_ui(key)
            self.assertEqual(value_in_xml, value_in_ui)

    @add_case_id("RHEL-113785")
    def test_cpu_memory_usage_info(self):
        self.open_vm_row()
        self.open_usage_subtab()
        self.assertNotEqual(self.get_cpu_usage_on_ui(), "0.0%")
        self.assertNotEqual(self.get_memory_usage_on_ui(), "0.00GiB")

    @add_case_id("RHEL-113787")
    def test_disks_info(self):
        self.get_dumpxml_on_host()
        self.open_vm_row()
        self.open_disks_subtab()
        disk_list = self.get_disk_list_in_xml()
        # disk_count_on_ui = self.get_disk_count_on_ui()
        # self.assertEqual(disk_count_on_ui, str(len(disk_list)))
        for disk in disk_list:
            for column in self.DISK_COLUMN_NAMES:
                target = self.get_disk_info_in_xml(disk, 'target')
                value_in_xml = self.get_disk_info_in_xml(disk, column)
                value_in_ui = self.get_disk_info_on_ui(target, column)
                self.assertEqual(value_in_xml, value_in_ui)

    @add_case_id("RHEL-118139")
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

    @add_case_id("RHEL-113788")
    def test_inline_vnc_console(self):
        self.open_vm_row()
        self.open_consoles_subtub()
        if self.check_inline_vnc_console():
            self.assert_frame_available(self.INLINE_CONSOLE_FRAME_NAME)
        else:
            self.assertEqual(self.get_console_type(), self.EXTERNAL_CONSOLE_NAME)

    @add_case_id("RHEL-113789")
    def test_ctrl_alt_del(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.open_consoles_subtub()
        if self.check_inline_vnc_console():
            self.send_ctrl_alt_del()
        else:
            self.assertEqual(self.get_console_type(), self.EXTERNAL_CONSOLE_NAME)

    @add_case_id("RHEL-118141")
    @add_case_id("RHEL-113793")
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

    @add_case_id("RHEL-113792")
    def test_external_console_more_info(self):
        self.open_vm_row()
        self.open_consoles_subtub()
        self.open_external_console_page()
        self.toggle_more_info()

    @add_case_id("RHEL-113794")
    def test_ovirt_info(self):
        self.open_vm_row()
        self.open_ovirt_subtub()
        for key in self.OVIRT_INFO_NAMES:
            value_in_host = self.get_ovirt_info_on_host(key)
            value_in_ui = self.get_ovirt_info_on_ui(key)
            self.assertEqual(value_in_host, value_in_ui)

    @add_case_id("RHEL-139377")
    def test_heVm_network_change(self):
        """
        :avocado: tags=heVM
        """
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Unplug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Plug')
        self.assertEqual(self.get_network1_state_on_ui(), 'down')
        self.assertEqual(self.get_network1_state_on_host(), 'down')

        self.prepare_network1_plug_button('Plug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Unplug')
        self.assertEqual(self.get_network1_state_on_ui(), 'up')
        self.assertEqual(self.get_network1_state_on_host(), 'up')

    @add_case_id("RHEL-118140")
    def test_ovirtVm_network_unplug(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Unplug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Plug')
        self.assertEqual(self.get_network1_state_on_ui(), 'down')
        self.assertEqual(self.get_network1_state_on_host(), 'down')

    @add_case_id("RHEL-139378")
    def test_ovirtVm_network_plug(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Plug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Unplug')
        self.assertEqual(self.get_network1_state_on_ui(), 'up')
        self.assertEqual(self.get_network1_state_on_host(), 'up')

    @add_case_id("RHEL-138481")
    def test_restart_heVm(self):
        """
        :avocado: tags=heVM
        """
        self.open_vm_row()
        self.reboot_he_vm_on_ui()

    @add_case_id("RHEL-138482")
    def test_force_reboot_heVm(self):
        """
        :avocado: tags=heVM
        """
        self.open_vm_row()
        self.force_reboot_he_vm_on_ui()

    @add_case_id("RHEL-138483")
    def test_shutdown_heVm(self):
        """
        :avocado: tags=heVM
        """
        self.open_vm_row()
        self.shutdown_he_vm_on_ui()

    @add_case_id("RHEL-138484")
    def test_forceoff_heVm(self):
        """
        :avocado: tags=heVM
        """
        self.open_vm_row()
        self.forceoff_he_vm_on_ui()

    @add_case_id("RHEL-139379")
    def test_sendnmi_heVm(self):
        """
        :avocado: tags=heVM
        """
        self.open_vm_row()
        self.sendnmi_he_vm_on_ui()

    @add_case_id("RHEL-139380")
    def test_supend_heVm(self):
        pass
        # self.open_vm_row()
        # self.suspend_he_vm_on_ui()

    @add_case_id("RHEL-113796")
    def test_restart_ovirtVm(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.reboot_ovirt_vm_on_ui()

    @add_case_id("RHEL-113797")
    def test_force_reboot_ovirtVm(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.force_reboot_ovirt_vm_on_ui()

    @add_case_id("RHEL-113798")
    def test_shutdown_ovirtVm(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.shutdown_ovirt_vm_on_ui()

    @add_case_id("RHEL-113799")
    def test_forceoff_ovirtVm(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.forceoff_ovirt_vm_on_ui()

    @add_case_id("RHEL-113800")
    def test_sendnmi_ovirtVm(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.sendnmi_ovirt_vm_on_ui()

    @add_case_id("RHEL-113820")
    def test_supend_ovirtVm(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.suspend_ovirt_vm_on_ui()

    def test_vdsm_conf_in_ui(self):
        self.check_vdsm_conf_in_ui()

    @add_case_id("RHEL-113776")
    def test_save_vdsm_conf_in_ui(self):
        self.check_save_vdsm_conf_in_ui()

    @add_case_id("RHEL-113777")
    def test_vdsm_service_link(self):
        self.click_vdsm_service_mgmt()

    @add_case_id("RHEL-113778")
    def test_reload_vdsm_conf(self):
        self.check_reload_vdsm_conf_in_ui()

    @add_case_id("RHEL-113781")
    def test_cluster_info(self):
        self.get_dumpxml_on_host()
        self.click(self.CLUSTER_TOPNAV)
        for key in self.CLUSTER_INFO_NAME:
            value_in_host = self.get_cluster_info_in_xml(key)
            value_in_ui = self.get_cluster_info_in_ui(key)
            self.assertEqual(value_in_host, value_in_ui)

    @add_case_id("RHEL-113782")
    def test_cluster_host_link(self):
        self.click(self.CLUSTER_TOPNAV)
        self.click_cluster_host_link()

    @add_case_id("RHEL-114121")
    def test_run_vm_in_cluster(self):
        """
        :avocado: tags=ovirtVM
        """
        self.open_vm_row()
        self.run_vm_in_cluster()

    @add_case_id("RHEL-118147")
    def test_template_info(self):
        self.click(self.TEMPLATES_TOPNAV)
        for key in self.TEMPLATE_INFO_NAME:
            value_in_host = self.get_template_info_on_host(key)
            value_in_ui = self.get_template_info_in_ui(key)
            self.assertEqual(value_in_host, value_in_ui)

    @add_case_id("RHEL-113779")
    def test_create_vm_by_template(self):
        self.click(self.TEMPLATES_TOPNAV)
        self.create_vm_by_template()

    @add_case_id("RHEL-113780")
    def test_create_vm_twice(self):
        self.click(self.TEMPLATES_TOPNAV)
        self.check_create_vm_twice()

    @add_case_id("RHEL-113786")
    def test_vm_icon(self):
        self.open_vm_row()
        self.assertEqual (self.get_vm_icon_data_on_host(), 
                self.get_vm_icon_data_on_ui())

    @add_case_id("RHEL-113974")
    def test_non_root_user(self):
        self.login_non_root_user()
        self.assert_element_invisible(self.VM_ROW)

    @add_case_id("RHEL-113795")
    def test_vm_migration(self):
        self.open_vm_row()
        self.open_ovirt_subtub()
        self.migrate_vm_to_additional_host()

    @add_case_id("RHEL-114114")
    def test_host_to_maintenance(self):
        self.host_to_maintenance()

    @add_case_id("RHEL-144275")
    def test_vcpu_count(self):
        self.open_vm_row()
        self.open_vcpu_details_window_on_host_page()
        values = self.get_vcpu_topology_on_engine()
        vcpu_count = int(values[0])*int(values[1])*int(values[2])
        self.assertEqual(self.get_vcpu_count_on_ui(), str(vcpu_count))

    @add_case_id("RHEL-144276")
    def test_change_vcpu_topology_on_cluster_page(self):
        """
        :avocado: tags=ovirtVM
        """
        self.shutdown_vm_on_engine()
        self.click(self.CLUSTER_TOPNAV)
        self.open_vcpu_details_window_on_cluster_page()
        self.set_vcpu_details_on_cluster_page('2', '1', '1')
        self.start_vm_on_cluster_page()
        self.assertEqual(self.get_vcpu_topology_on_engine(), ['2', '1', '1'])

