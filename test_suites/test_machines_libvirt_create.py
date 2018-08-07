import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_machines_libvirt_create import PageMachinesLibvirtCreate


class TestMachinesLibvirtCreate(PageMachinesLibvirtCreate):
    """
    :avocado: enable
    :avocado: tags=machines_create
    """

    def test_create_vm_with_iso(self):
        self.create_new_vm('vm_iso',
                           location=self.params.get('iso_file'),
                           memory_size='2',
                           storage_size='2',
                           os_vendor='CentOS',
                           os_name='CentOS 7.0')
        self.assert_element_visible(self.VM_ROW.format(self.vmname))
        vm_state = self.VM_STATE.format(self.vmname)
        self.assert_in_text(vm_state, 'creating VM')
        self.assert_element_visible(self.VCPU_DETAILS_LINK.format(self.vmname))
        self.assert_in_text(vm_state, 'shut off')
        self.install_vm()
        self.assert_in_text(vm_state, 'creating VM installation')
        self.assert_in_text(vm_state, 'running')
        self.assert_frame_available(
            self.INLINE_CONSOLE_FRAME_NAME.format(self.vmname))

    def test_create_vm_with_url(self):
        self.create_new_vm('vm_url',
                           is_filesystem_location=False,
                           location=self.params.get('valid_url'),
                           memory_size='1000',
                           memory_size_unit="MiB",
                           storage_size='1',
                           os_vendor='Unspecified',
                           os_name='Other OS',
                           start_vm=True)
        self.assert_element_visible(self.VM_ROW.format(self.vmname))
        vm_state = self.VM_STATE.format(self.vmname)
        self.assert_in_text(vm_state, 'creating VM installation')
        self.assert_in_text(vm_state, 'running')
        self.assert_frame_available(
            self.INLINE_CONSOLE_FRAME_NAME.format(self.vmname))

    def test_configure_vcpu_when_create_vm(self):
        self.create_new_vm('vm_vcpu',
                           location=self.params.get('iso_file'),
                           memory_size='1',
                           storage_size='1000',
                           storage_size_unit="MiB",
                           os_vendor='Unspecified',
                           os_name='Other OS')
        self.wait_before_install()
        self.open_vcpu_details_window()
        self.assert_element_invisible(self.VCPU_CAUTION)
        self.set_vcpu_details('8', '4', '2', '2', '2')
        self.assert_element_invisible(self.VCPU_DETAILS_WINDOW)
        self.assertEqual(self.get_vcpu_count_on_ui(), '4')
        self.install_vm()
        self.wait_after_install()

    def test_delete_vm_with_storage(self):
        self.create_new_vm('vm_delete',
                           location=self.params.get('iso_file'),
                           memory_size='1',
                           storage_size='1',
                           os_vendor='Unspecified',
                           os_name='Other OS')
        self.wait_before_install()
        self.assertIn("vm_delete.qcow2", self.get_storage_list_on_host())
        self.delete_vm_on_ui()
        self.assert_element_invisible(self.VM_ROW.format(self.vmname))
        self.assertNotIn(self.vmname, self.get_vm_list_on_host())
        self.assertNotIn("vm_delete.qcow2", self.get_storage_list_on_host())

    def test_create_many_vms(self):
        for i in range(0, 20):
            self.create_new_vm('vm_{}'.format(i),
                               location=self.params.get('iso_file'),
                               memory_size='1',
                               memory_size_unit="MiB",
                               storage_size='1',
                               storage_size_unit="MiB",
                               os_vendor='Unspecified',
                               os_name='Other OS')
            self.wait_before_install()

    def test_delete_all_vms(self):
        vm_list = ['vm_iso', 'vm_url', 'vm_vcpu']
        for i in range(0, 20):
            vm_list.append('vm_{}'.format(i))
        for vm in vm_list:
            self.vmname = vm
            self.prepare_no_vm()
            storage = "/var/lib/libvirt/images/{}.qcow2".format(vm)
            cmd = "test -e {disk_file} && rm -f {disk_file}".format(
                disk_file=storage)
            self.host.execute(cmd, raise_exception=False)
