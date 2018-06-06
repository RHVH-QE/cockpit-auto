import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_machines_check import MachinesCheckPage


class TestMachinesCheck(MachinesCheckPage):
    """
    :avocado: enable
    :avocado: tags=machines
    """

    def test_no_vm(self):
        self.prepare_no_vm()
        self.assertEqual(self.get_no_vm_text_on_ui(), self.NO_VM_TEXT)

    def test_memory_usage_off(self):
        self.prepare_stop_vm()
        self.open_vm_row()
        self.open_usage_subtab()
        self.assertEqual(self.get_memory_usage_on_ui(), "0.00GiB")

    def test_cpu_usage_off(self):
        self.prepare_stop_vm()
        self.open_vm_row()
        self.open_usage_subtab()
        self.assertEqual(self.get_cpu_usage_on_ui(), "0.0%")

    def test_disk_notification(self):
        self.prepare_stop_vm()
        self.open_vm_row()
        self.open_disks_subtab()
        self.assert_element_visible(self.DISKS_NOTIFICATION)

    def test_vm_status(self):
        self.prepare_running_vm()
        value_on_host = self.get_vm_state_on_host()
        value_on_ui = self.get_vm_state_on_ui()
        self.assertEqual(value_on_host, value_on_ui)

    def test_overview_info(self):
        self.prepare_running_vm()
        self.get_dumpxml_on_host()
        self.open_vm_row()
        for key in self.OVERVIEW_INFO_NAMES:
            value_in_xml = self.get_overview_info_in_xml(key)
            value_on_ui = self.get_overview_info_on_ui(key)
            self.assertEqual(value_in_xml, value_on_ui)

    def test_disks_info(self):
        self.prepare_running_vm()
        self.get_dumpxml_on_host()
        self.open_vm_row()
        self.open_disks_subtab()
        disk_list = self.get_disk_list_in_xml()
        disk_count_on_ui = self.get_disk_count_on_ui()
        self.assertEqual(disk_count_on_ui, str(len(disk_list)))
        for disk in disk_list:
            target = self.get_disk_info_in_xml(disk, 'target')
            for column in self.DISK_COLUMN_NAMES:
                value_in_xml = self.get_disk_info_in_xml(disk, column)
                value_on_ui = self.get_disk_info_on_ui(target, column)
                self.assertEqual(value_in_xml, value_on_ui)

    def test_networks_info(self):
        self.prepare_running_vm()
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

    def test_network_unplug(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Unplug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Plug')
        self.assertEqual(self.get_network1_state_on_ui(), 'down')
        self.assertEqual(self.get_network1_state_on_host(), 'down')

    def test_network_plug(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_networks_subtab()
        self.prepare_network1_plug_button('Plug')
        self.click_network1_plug_button()
        self.assertEqual(self.get_network1_plug_button_text(), 'Unplug')
        self.assertEqual(self.get_network1_state_on_ui(), 'up')
        self.assertEqual(self.get_network1_state_on_host(), 'up')

    def test_sendnmi_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.sendnmi_vm_on_ui()
        self.assertEqual(self.get_vm_state_on_ui(), 'running')
        self.assert_element_invisible(self.SENDNMI_BUTTON)

    def test_shutdown_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.shutdown_vm_on_ui()
        self.assert_element_visible(self.RUN_BUTTON)
        self.assertEqual(self.get_vm_state_on_ui(), 'shut off')
        self.assertEqual(self.get_vm_state_on_host(), 'shut off')

    def test_run_vm(self):
        self.prepare_stop_vm()
        self.open_vm_row()
        self.run_vm_on_ui()
        self.assert_element_visible(self.RESTART_BUTTON)
        self.assertEqual(self.get_vm_state_on_ui(), 'running')
        self.assertEqual(self.get_vm_state_on_host(), 'running')

    def test_forceoff_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.forceoff_vm_on_ui()
        self.assert_element_visible(self.RUN_BUTTON)
        self.assertEqual(self.get_vm_state_on_ui(), 'shut off')
        self.assertEqual(self.get_vm_state_on_host(), 'shut off')

    def test_delete_vm_without_storage(self):
        self.prepare_stop_vm()
        self.open_vm_row()
        self.open_delete_vm_dialog()
        self.check_storage_box()
        self.delete_vm_on_ui()
        self.assert_element_invisible(self.VM_ROW)
        self.assertNotIn(self.VM_NAME, self.get_vm_list_on_host())
