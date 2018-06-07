from time import sleep
import xmltodict
from seleniumlib import SeleniumTest
from utils.machine import RunCmdError


class MachinesCheckPage(SeleniumTest):
    """
    :avocado: disable
    """
    VM_NAME = "vmtest"
    WAIT_VM_UP = 10
    WATI_VM_DOWN = 5

    MACHINES_LINK = "#sidebar-menu a[href='/machines']"
    MACHINES_FRAME_NAME = "/machines"

    NO_VM_EL = "#app tr td"
    NO_VM_TEXT = 'No VM is running or defined on this host'

    # id prefix, {} should be the actual vm name
    _ID_PREFIX = "#vm-{}-".format(VM_NAME)
    VM_ROW = _ID_PREFIX + 'row'
    VM_STATE = _ID_PREFIX + 'state'
    RUN_BUTTON = _ID_PREFIX + 'run'
    RESTART_BUTTON = _ID_PREFIX + 'reboot'
    SHUTDOWN_BUTTON = _ID_PREFIX + 'off'
    SHUTDOWN_DROPDOWN_BUTTON = SHUTDOWN_BUTTON + '-caret'
    FORCEOFF_BUTTON = _ID_PREFIX + 'forceOff'
    SENDNMI_BUTTON = _ID_PREFIX + 'sendNMI'
    DELETE_BUTTON = _ID_PREFIX + 'delete'
    DELETE_STORAGE_CHECKBOX = "input[type=checkbox]"
    DELETE_VM_BUTTON = "#cockpit_modal_dialog .modal-footer button:nth-of-type(2)"

    # overview subtab
    OVERVIEW_INFO_NAMES = ['memory', 'vcpus',
                           'cputype', 'emulatedmachine', 'bootorder', 'autostart']

    # usage subtab
    USAGE_TAB = _ID_PREFIX + "usage"
    USED_MEMORY_VALUE = "#chart-donut-0 .donut-title-big-pf"
    USED_MEMORY_UNIT = "#chart-donut-0 .donut-title-small-pf"
    USED_CPU_VALUE = "#chart-donut-1 .donut-title-big-pf"
    USED_CPU_UNIT = "#chart-donut-1 .donut-title-small-pf"

    # disks subtab
    DISKS_TAB = _ID_PREFIX + "disks"
    DISKS_NOTIFICATION = DISKS_TAB + "-notification"
    DISKS_COUNT = DISKS_TAB + "-total-value"
    DISK_COLUMN_TEMPLATE = DISKS_TAB + "-{}-"
    DISK_COLUMN_NAMES = ['device', 'target', 'bus', 'readonly', 'source']
    DISK_COLUMN_READONLY = "//*[@id='{}bus']//parent::*//following-sibling::*"
    DISK_COLUMN_SOURCE = "{}source .machines-disks-source-value"

    # networks subtab
    NETWORKS_TAB = _ID_PREFIX + "networks"
    NETWORK_COLUMN_TEMPLATE = _ID_PREFIX + "network" + "-{}-"
    NETWORK_COLUMN_NAMES = ['type', 'model',
                            'mac', 'target', 'source', 'state']
    NETWORK1_PLUG_BUTTON = "#vm-{}-network-1-state button".format(VM_NAME)

    def open_page(self):
        self.click(self.MACHINES_LINK)
        self.switch_to_frame(self.MACHINES_FRAME_NAME)

    def open_vm_row(self):
        self.click(self.VM_ROW)

    def open_usage_subtab(self):
        # self.click(self.USAGE_TAB)
        self.hover_and_click(self.USAGE_TAB)

    def open_disks_subtab(self):
        self.hover_and_click(self.DISKS_TAB)
        sleep(2)

    def open_networks_subtab(self):
        self.hover_and_click(self.NETWORKS_TAB)

    def run_vm_on_ui(self):
        self.click(self.RUN_BUTTON)

    def shutdown_vm_on_ui(self):
        self.click(self.SHUTDOWN_BUTTON)
        sleep(self.WATI_VM_DOWN)

    def forceoff_vm_on_ui(self):
        self.click(self.SHUTDOWN_DROPDOWN_BUTTON)
        self.click(self.FORCEOFF_BUTTON)

    def sendnmi_vm_on_ui(self):
        self.click(self.SHUTDOWN_DROPDOWN_BUTTON)
        self.click(self.SENDNMI_BUTTON)

    def open_delete_vm_dialog(self):
        self.click(self.DELETE_BUTTON)

    def check_storage_box(self):
        self.click(self.DELETE_STORAGE_CHECKBOX)

    def delete_vm_on_ui(self):
        self.click(self.DELETE_VM_BUTTON)

    def prepare_running_vm(self):
        state = self.get_vm_state_on_host()
        if not state:
            self.create_running_vm_by_virsh()
        elif state == 'shut off':
            self.start_vm_by_virsh()

    def prepare_stop_vm(self):
        state = self.get_vm_state_on_host()
        if not state:
            self.create_stop_vm_by_virsh()
        if state == 'running':
            self.stop_vm_by_virsh()

    def prepare_no_vm(self):
        state = self.get_vm_state_on_host()
        if 'running' == state:
            self.destroy_vm_by_virsh()
        elif 'shut off' == state:
            self.undefine_vm_by_virsh()

    def create_running_vm_by_virsh(self):
        """
        The vm.xml and vm.qcow2 should be copied to host beforehand,
        vm.qcow2 should be installed with OS.
        """
        cmd = 'virsh create /var/lib/libvirt/images/vm.xml'
        self.host.execute(cmd)
        # wait for guest os to start up.
        sleep(self.WAIT_VM_UP)

    def create_stop_vm_by_virsh(self):
        cmd = 'virsh define /var/lib/libvirt/images/vm.xml'
        self.host.execute(cmd)

    def start_vm_by_virsh(self):
        cmd = 'virsh start {}'.format(self.VM_NAME)
        self.host.execute(cmd)
        sleep(self.WAIT_VM_UP)

    def stop_vm_by_virsh(self):
        cmd = 'virsh shutdown {}'.format(self.VM_NAME)
        self.host.execute(cmd)
        sleep(self.WATI_VM_DOWN)

    def destroy_vm_by_virsh(self):
        cmd = 'virsh destroy {}'.format(self.VM_NAME)
        self.host.execute(cmd)

    def undefine_vm_by_virsh(self):
        cmd = 'virsh undefine {}'.format(self.VM_NAME)
        self.host.execute(cmd)

    def get_no_vm_text_on_ui(self):
        return self.get_text(self.NO_VM_EL)

    def get_vm_list_on_host(self):
        cmd = 'virsh list --all'
        return self.host.execute(cmd)

    def get_dumpxml_on_host(self):
        cmd = 'virsh dumpxml {}'.format(self.VM_NAME)
        ret = self.host.execute(cmd)
        self.vm_xml_info = xmltodict.parse(ret)

    def get_vm_state_on_host(self):
        cmd = 'virsh domstate {}'.format(self.VM_NAME)
        try:
            ret = self.host.execute(cmd)
            return ret.split('\n')[0]
        except RunCmdError:
            return None

    def get_vm_state_on_ui(self):
        return self.get_text(self.VM_STATE)

    def get_autostart_state_on_host(self):
        cmd = 'virsh dominfo {} | grep -i autostart'.format(self.VM_NAME)
        ret = self.host.execute(cmd)
        return ret.split(' ')[-1]

    def get_overview_info_in_xml(self, key):
        if key == 'memory':
            value = int(self.vm_xml_info['domain']
                        ['memory']['#text']) / (1024 * 1024)
        if key == 'vcpus':
            value = self.vm_xml_info['domain']['vcpu']['#text']
        if key == 'cputype':
            mode = self.vm_xml_info['domain']['cpu']['@mode']
            model = self.vm_xml_info['domain']['cpu']['model']['#text']
            value = mode + " (" + model + ")"
        if key == 'emulatedmachine':
            value = self.vm_xml_info['domain']['os']['type']['@machine']
        if key == 'bootorder':
            value_list = []
            for boot in self.vm_xml_info['domain']['os']['boot']:
                dev = boot['@dev']
                if dev == 'hd':
                    dev = 'disk'
                value_list.append(dev)
            value = ','.join(value_list)
        if key == 'autostart':
            value = self.get_autostart_state_on_host() + 'd'
        return value

    def get_overview_info_on_ui(self, key):
        el_descriptor = self._ID_PREFIX + key
        value = self.get_text(el_descriptor)
        if key == 'memory':
            value = int(value.split(' ')[0])
        return value

    def get_disk_list_in_xml(self):
        value = []
        ret = self.vm_xml_info['domain']['devices']['disk']
        if not isinstance(ret, list):
            value.append(ret)
        else:
            value = ret
        return value

    def get_disk_info_in_xml(self, disk, key):
        if key == 'device':
            value = disk['@device']
        if key == 'target':
            value = disk['target']['@dev']
        if key == 'bus':
            value = disk['target']['@bus']
        if key == 'readonly':
            if 'readonly' in disk:
                value = 'yes'
            else:
                value = 'no'
        if key == 'source':
            value = disk['source']['@file']
        return value

    def get_disk_info_on_ui(self, target, column):
        disk = self.DISK_COLUMN_TEMPLATE.format(target)
        if column == 'readonly':
            el_descriptor = self.DISK_COLUMN_READONLY.format(disk.lstrip('#'))
        elif column == 'source':
            el_descriptor = self.DISK_COLUMN_SOURCE.format(disk)
        else:
            el_descriptor = disk + column
        return self.get_text(el_descriptor)

    def get_disk_count_on_ui(self):
        return self.get_text(self.DISKS_COUNT)

    def get_network_list_in_xml(self):
        value = []
        ret = self.vm_xml_info['domain']['devices']['interface']
        if not isinstance(ret, list):
            value.append(ret)
        else:
            value = ret
        return value

    def get_network_state_on_host(self, interface):
        cmd = 'virsh domif-getlink {} {}'.format(self.VM_NAME, interface)
        ret = self.host.execute(cmd)
        return ret.split(' ')[-1]

    def get_network_info_in_xml(self, network, key):
        if key == 'type':
            value = network['@type']
        if key == 'model':
            value = network['model']['@type']
        if key == 'mac':
            value = network['mac']['@address']
        if key == 'target':
            value = network['target']['@dev']
        if key == 'source':
            net_type = '@' + network['@type']
            value = network['source'][net_type]
        if key == 'state':
            interface = network['target']['@dev']
            value = self.get_network_state_on_host(interface)
        if key == 'button':
            interface = network['target']['@dev']
            state = self.get_network_state_on_host(interface)
            if state == 'up':
                value = 'Unplug'
            else:
                value = 'Plug'
        return value

    def get_network_info_on_ui(self, seq_num, column):
        if column in ['source', 'state', 'button']:
            parent = column
            son = 'span'
            if column == 'button':
                parent = 'state'
                son = 'button'
            parent_id = self.NETWORK_COLUMN_TEMPLATE.format(seq_num) + parent
            el_descriptor = "{} {}".format(parent_id, son)
        else:
            el_descriptor = self.NETWORK_COLUMN_TEMPLATE.format(
                seq_num) + column
        return self.get_text(el_descriptor)

    def get_network1_state_on_ui(self):
        return self.get_network_info_on_ui('1', 'state')

    def get_network1_plug_button_text(self):
        return self.get_network_info_on_ui('1', 'button')

    def click_network1_plug_button(self):
        self.click(self.NETWORK1_PLUG_BUTTON)
        sleep(2)

    def prepare_network1_plug_button(self, expected_text):
        plug_text = self.get_network1_plug_button_text()
        if plug_text != expected_text:
            self.click_network1_plug_button()

    def get_network1_state_on_host(self):
        target = self.get_network_info_on_ui('1', 'target')
        return self.get_network_state_on_host(target)

    def get_memory_usage_on_ui(self):
        value = self.get_text(self.USED_MEMORY_VALUE)
        unit = self.get_text(self.USED_MEMORY_UNIT)
        return value + unit

    def get_cpu_usage_on_ui(self):
        value = self.get_text(self.USED_CPU_VALUE)
        unit = self.get_text(self.USED_CPU_UNIT)
        return value + unit
