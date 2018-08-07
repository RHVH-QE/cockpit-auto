import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_machines_libvirt_check import PageMachinesLibvirtCheck


class TestMachinesLibvirtCheck(PageMachinesLibvirtCheck):
    """
    :avocado: enable
    :avocado: tags=machines_check
    """

    def test_prepare_files(self):
        root_dir = "/var/lib/libvirt/images"
        for f in ['staticvm.xml', 'staticvm.qcow2']:
            cmd = 'test -e {}/{}'.format(root_dir, f)
            ret = self.host.execute(cmd, raise_exception=False)
            if not ret.succeeded:
                local_path = self.get_data(f)
                self.host.put_file(local_path, root_dir)
                if f == 'staticvm.xml':
                    if re.match(r'^10.', self.host.host_string):
                        ip = self.host.host_string
                    else:
                        cmd = ("ip -f inet addr show | grep 'inet 10.' | "
                               "awk '{print $2}'| awk -F '/' '{print $1}'")
                        ip = self.host.execute(cmd)
                    cmd = "sed -i 's/127.0.0.1/{}/g' {}/{}".format(
                        ip, root_dir, f)
                    self.host.execute(cmd)

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
        self.open_disks_subtab(state='stop')
        self.assert_element_visible(
            self.DISKS_NOTIFICATION.format(self.vmname))

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

    def test_memory_usage_running(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_usage_subtab()
        self.assertNotEqual(self.get_memory_usage_on_ui(
            state='running'), "0.00GiB")

    def test_cpu_usage_running(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_usage_subtab()
        self.assertNotEqual(self.get_cpu_usage_on_ui(state='running'), "0.0%")

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

    def test_inline_console(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_consoles_subtab()
        self.assertEqual(self.get_console_type(), self.INLINE_CONSOLE_TYPE)
        self.assert_frame_available(
            self.INLINE_CONSOLE_FRAME_NAME.format(self.vmname))
        self.send_ctrl_alt_del()
        self.assertTrue(self.wait_canvas_change())

    def test_external_console(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_consoles_subtab()
        self.open_external_console_page()
        self.assertEqual(self.get_console_type(), self.EXTERNAL_CONSOLE_NAME)
        viewer_info_list = self.get_external_console_info_in_xml()
        # test launch remote viewer function
        self.launch_remote_viewer()
        self.assertEqual(self.get_external_console_info_in_vv(), self.VV_FILE_ATTR.format(
            viewer_info_list[0]['ip'], viewer_info_list[0]['port']))
        # test more infor link
        self.toggle_more_info()
        # test manual connection info
        self.assertEqual(self.get_consoles_manual_address_on_ui(),
                         viewer_info_list[0]['ip'])
        for viewer in viewer_info_list:
            self.assertEqual(self.get_consoles_manual_port_on_ui(
                viewer['type']), viewer['port'])

    def test_serial_console(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_consoles_subtab()
        self.open_serial_console_page()
        self.assertEqual(self.get_console_type(), self.SERIAL_CONSOLE_NAME)
        self.assert_element_visible(self.SERIAL_CANVAS)
        self.disconnect_serial_console()
        self.reconnect_serial_console()
        self.assert_element_visible(self.SERIAL_CANVAS)

    def test_sendnmi_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.sendnmi_vm_on_ui()
        self.assertEqual(self.get_vm_state_on_ui(), 'running')
        self.assert_element_invisible(self.SENDNMI_BUTTON.format(self.vmname))

    def test_shutdown_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.shutdown_vm_on_ui()
        self.assert_element_visible(self.RUN_BUTTON.format(self.vmname))
        self.assertEqual(self.get_vm_state_on_ui(), 'shut off')
        self.assertEqual(self.get_vm_state_on_host(), 'shut off')

    def test_run_vm(self):
        self.prepare_stop_vm()
        self.open_vm_row()
        self.run_vm_on_ui()
        self.assert_element_visible(self.RESTART_BUTTON.format(self.vmname))
        self.assertEqual(self.get_vm_state_on_ui(), 'running')
        self.assertEqual(self.get_vm_state_on_host(), 'running')

    def test_restart_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.restart_vm_on_ui()
        self.open_consoles_subtab()
        self.assertTrue(self.wait_canvas_change())

    def test_force_restart_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.force_restart_vm_on_ui()
        self.open_consoles_subtab()
        self.assertTrue(self.wait_canvas_change())

    def test_non_root_operation(self):
        self.prepare_running_vm()
        self.login_non_root_user()
        self.open_page()
        self.open_vm_row()
        self.restart_vm_on_ui()
        self.assertEqual(self.get_last_message_text(), self.RESTART_ALERT_TEXT)
        self.force_restart_vm_on_ui()
        self.assertEqual(self.get_last_message_text(),
                         self.FORCE_RESTART_ALERT_TEXT)
        self.shutdown_vm_on_ui()
        self.assertEqual(self.get_last_message_text(),
                         self.SHUTDOWN_ALERT_TEXT)
        self.forceoff_vm_on_ui()
        self.assertEqual(self.get_last_message_text(),
                         self.FORCE_SHUTDOWN_ALERT_TEXT)
        self.sendnmi_vm_on_ui()
        self.assertEqual(self.get_last_message_text(),
                         self.SEND_NMI_ALEART_TEXT)
        self.delete_vm_on_ui()
        self.assertEqual(self.get_delete_vm_alert_text(),
                         self.DELETE_VM_ALEART_TEXT)

    def test_change_vcpu_of_running_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.open_vcpu_details_window()
        self.assert_element_visible(self.VCPU_CAUTION)
        self.set_vcpu_details('8', '4', '2', '2', '2')
        self.assert_element_invisible(self.VCPU_DETAILS_WINDOW)
        self.assertNotEqual(self.get_vcpu_count_on_ui(), '4')
        self.shutdown_vm_on_ui()
        self.wait_visible(self.RUN_BUTTON.format(self.vmname))
        self.run_vm_on_ui()
        self.wait_visible(self.RESTART_BUTTON.format(self.vmname))
        self.assertEqual(self.get_vcpu_count_on_ui(), '4')
        self.assertEqual(self.get_vcpu_topology_in_xml(), ['2', '2', '2'])

    def test_force_off_vm(self):
        self.prepare_running_vm()
        self.open_vm_row()
        self.forceoff_vm_on_ui()
        self.assert_element_visible(self.RUN_BUTTON.format(self.vmname))
        self.assertEqual(self.get_vm_state_on_ui(), 'shut off')
        self.assertEqual(self.get_vm_state_on_host(), 'shut off')

    def test_delete_vm_without_storage(self):
        self.prepare_stop_vm()
        self.open_vm_row()
        self.delete_vm_on_ui(del_storage=False)
        self.assert_element_invisible(self.VM_ROW.format(self.vmname))
        self.assertNotIn(self.vmname, self.get_vm_list_on_host())
