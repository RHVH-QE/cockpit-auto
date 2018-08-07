from page_machines_libvirt_check import PageMachinesLibvirtCheck as COMM
from time import sleep


class PageMachinesLibvirtCreate(COMM):
    """
    :avocado: disable
    """
    CREATE_NEW_VM_BUTTON = "#create-new-vm"

    # vm creation dialogue
    NAME = "#vm-name"
    INSTALL_SOURCE_TYPE = "#source-type"
    INSTALL_SOURCE_FILE_INPUT = "#source-file input"
    INSTALL_SOURCE_ITEM = "//*[@id='source-file']//a[text()='test.iso']"
    INSTALL_SOURCE_URL_INPUT = "#source-url"
    OS_VENDER = "#vendor-select"
    OPERATING_SYSTEM = "#system-select"
    MEMORY_SIZE_INPUT = "#memory-size"
    MEMORY_UNIT = "#memory-size-unit-select"
    STORAGE_SIZE_INPUT = "#storage-size"
    STORAGE_UNIT = "#storage-size-unit-select"
    START_VM_CHECKBOX = "#start-vm"
    CREATE_BUTTON = ".modal-footer button.apply"
    CANCEL_BUTTON = ".modal-footer button.cancel"

    # Install vm
    INSTALL_BUTTON = COMM._ID_PREFIX + 'install'

    def create_new_vm(self, name, is_filesystem_location=True, location='',
                      memory_size=1, memory_size_unit='GiB',
                      storage_size=1, storage_size_unit='GiB',
                      os_vendor=None,
                      os_name=None,
                      start_vm=False):

        self.vmname = name
        self.click(self.CREATE_NEW_VM_BUTTON)
        self.input_text(self.NAME, name)

        if is_filesystem_location:
            self._prepare_iso_on_host(location)
            self._select_from_dropdown(
                self.INSTALL_SOURCE_TYPE, 'Filesystem')
            self.input_text(self.INSTALL_SOURCE_FILE_INPUT, location)
            self.wait_present(self.INSTALL_SOURCE_ITEM)
        else:
            self._select_from_dropdown(
                self.INSTALL_SOURCE_TYPE, 'URL')
            self.input_text(self.INSTALL_SOURCE_URL_INPUT, location)

        self._select_from_dropdown(self.OS_VENDER, os_vendor)
        self._select_from_dropdown(self.OPERATING_SYSTEM, os_name)

        self.input_text(self.MEMORY_SIZE_INPUT, memory_size)
        self._select_from_dropdown(self.MEMORY_UNIT, memory_size_unit)

        self.input_text(self.STORAGE_SIZE_INPUT, storage_size)
        self._select_from_dropdown(self.STORAGE_UNIT, storage_size_unit)

        if start_vm:
            self.click(self.START_VM_CHECKBOX)
        self.click(self.CREATE_BUTTON)

    def install_vm(self):
        self.click(self.INSTALL_BUTTON.format(self.vmname))

    def wait_before_install(self):
        self.wait_visible(self.VM_ROW.format(self.vmname))
        vm_state = self.VM_STATE.format(self.vmname)
        self.wait_in_text(vm_state, 'creating VM')
        self.wait_visible(self.VCPU_DETAILS_LINK.format(self.vmname))
        self.wait_in_text(vm_state, 'shut off')

    def wait_after_install(self):
        vm_state = self.VM_STATE.format(self.vmname)
        self.wait_in_text(vm_state, 'creating VM installation')
        self.wait_in_text(vm_state, 'running')
        self.switch_to_frame(
            self.INLINE_CONSOLE_FRAME_NAME.format(self.vmname))

    def _select_from_dropdown(self, selector, value):
        button = "{} button span:nth-of-type(1)".format(selector)
        if self.get_text(button) != value:
            item_selector = "{} ul li[data-value*={}] a".format(
                selector, value)
            self.click(button)
            self.wait_visible(item_selector)
            self.click(item_selector)
            self.wait_in_text(button, value)

    def _prepare_iso_on_host(self, iso_file):
        cmd = 'test -e {}'.format(iso_file)
        ret = self.host.execute(cmd, raise_exception=False)
        if not ret.succeeded:
            cmd = 'touch {}'.format(iso_file)
            self.host.execute(cmd)

    def get_storage_list_on_host(self):
        cmd = "ls /var/lib/libvirt/images"
        return self.host.execute(cmd)
