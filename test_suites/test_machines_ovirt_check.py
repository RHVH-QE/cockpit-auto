import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_machines_ovirt_check import MachinesOvirtCheckPage


class TestMachinesOvirtCheck(MachinesOvirtCheckPage):
    """
    :avocado: enable
    :avocado: tags=machines-ovirt
    """

    def test_disable_create_new_vm(self):
        """
        :avocado: tags=ovirt
        """
        self.disable_create_new_vm()

    def test_host_to_maintenance(self):
        """
        :avocado: tags=ovirt
        """
        self.host_to_maintenance()

    def test_overview_info(self):
        """
        :avocado: tags=ovirt
        """
        self.get_dumpxml_on_host()
        self.open_vm_row()
        for key in self.OVERVIEW_INFO_NAMES:
            value_in_xml = self.get_overview_info_in_xml(key)
            value_in_ui = self.get_overview_info_on_ui(key)
            self.assertEqual(value_in_xml, value_in_ui)

    def test_disks_info(self):
        """
        :avocado: tags=ovirt
        """
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
        """
        :avocado: tags=ovirt
        """
        self.get_vmxml_on_host()
        self.open_vm_row()
        self.open_networks_subtab()
        network_list = self.get_network_list_in_xml()
        for i in range(len(network_list)):
            network = network_list[i]
            for column in self.NETWORK_COLUMN_NAMES:
                value_in_xml = self.get_network_info_in_xml(network, column)
                value_on_ui = self.get_network_info_on_ui(i + 1, column)
                self.assertEqual(value_in_xml, value_on_ui)

    def test_ovirt_info(self):
        """
        :avocado: tags=ovirt
        """
        self.open_vm_row()
        self.open_ovirt_subtub()
        for key in self.OVIRT_INFO_NAMES: 
            value_in_host = self.get_ovirt_info_on_host(key)
            value_in_ui = self.get_ovirt_info_on_ui(key)
            self.assertEqual(value_in_host, value_in_ui)

    def test_vm_migration(self):
        """
        :avocado: tags=ovirt
        """
        self.open_vm_row()
        self.open_ovirt_subtub()
        self.migrate_vm_to_additional_host()

    def test_network_plug(self):
        """
        :avocado: tags=ovirt
        """
        # The Plug/Unplug shouldn't be successfully
        self.open_vm_row()
        self.open_networks_subtab()
        self.click_network1_plug_button()

    def test_restart_vm(self):
        """
        :avocado: tags=ovirt
        """
        self.open_vm_row()
        self.reboot_vm_on_ui()

    def test_force_reboot_vm(self):
        """
        :avocado: tags=ovirt
        """
        self.open_vm_row()
        self.force_reboot_vm_on_ui()

    def test_shutdown_vm(self):
        """
        :avocado: tags=ovirt
        """
        self.open_vm_row()
        self.shutdown_vm_on_ui()

    def test_forceoff_vm(self):
        """
        :avocado: tags=ovirt
        """
        self.open_vm_row()
        self.forceoff_vm_on_ui()

    def test_sendnmi_vm(self):
        """
        avocado: tags=ovirt
        """
        self.open_vm_row()
        self.sendnmi_vm_on_ui()






