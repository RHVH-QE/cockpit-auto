from time import sleep
import xmltodict
from seleniumlib import SeleniumTest
from utils.machine import RunCmdError


class PageMachinesLibvirtCheck(SeleniumTest):
    """
    :avocado: disable
    """
    WAIT_VM_UP = 10
    WATI_VM_DOWN = 5

    MACHINES_LINK = "#sidebar-menu a[href='/machines']"
    MACHINES_FRAME_NAME = "/machines"

    NO_VM_EL = "#app tr td"
    NO_VM_TEXT = 'No VM is running or defined on this host'

    # id prefix, {} should be the actual vm name
    _ID_PREFIX = "#vm-{}-"
    VM_ROW = _ID_PREFIX + 'row'
    VM_STATE = _ID_PREFIX + 'state'

    # operation button
    RUN_BUTTON = _ID_PREFIX + 'run'
    RESTART_BUTTON = _ID_PREFIX + 'reboot'
    RESTART_DROPDOWN_BUTTON = RESTART_BUTTON + '-caret'
    FORCE_RESTART_BUTTON = _ID_PREFIX + 'forceReboot'
    SHUTDOWN_BUTTON = _ID_PREFIX + 'off'
    SHUTDOWN_DROPDOWN_BUTTON = SHUTDOWN_BUTTON + '-caret'
    FORCEOFF_BUTTON = _ID_PREFIX + 'forceOff'
    SENDNMI_BUTTON = _ID_PREFIX + 'sendNMI'
    DELETE_BUTTON = _ID_PREFIX + 'delete'
    DELETE_STORAGE_CHECKBOX = "input[type=checkbox]"
    DELETE_VM_BUTTON = "#cockpit_modal_dialog .modal-footer button:nth-of-type(2)"

    # overview subtab
    OVERVIEW_INFO_NAMES = ['memory', 'vcpus-count',
                           'cputype', 'emulatedmachine', 'bootorder', 'autostart']
    VCPU_DETAILS_LINK = _ID_PREFIX + 'vcpus-count'
    VCPU_DETAILS_WINDOW = ".vcpu-detail-modal-table"
    VCPU_CAUTION = "td.machines-vcpu-caution"
    VCPU_MAXIMUM_INPUT = "#machines-vcpu-max-field"
    VCPU_COUNT_INPUT = "#machines-vcpu-count-field"
    VCPU_SOCKETS_SELECT_BUTTON = "#socketsSelect"
    VCPU_SOCKETS_ITEM = "#socketsSelect ul li:nth-of-type({})"
    VCPU_CORES_SELECT_BUTTON = "#coresSelect"
    VCPU_CORES_ITEM = "#coresSelect ul li:nth-of-type({})"
    VCPU_THREADS_SELECT_BUTTON = "#threadsSelect"
    VCPU_THREADS_ITEM = "#threadsSelect ul li:nth-of-type({})"
    VCPU_APPLY_BUTTON = "button.apply"

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
    NETWORK1_STATE = "#vm-{}-network-1-state span"
    NETWORK1_PLUG_BUTTON = "#vm-{}-network-1-state button"
    NETWORK1_TARGET = "#vm-{}-network-1-target"

    # consoles subtab
    CONSOLES_TAB = _ID_PREFIX + "consoles"
    CONSOLE_TYPE_BUTTON = "#console-type-select button"
    CONSOLE_TYPE_TEXT = "#console-type-select button span:nth-of-type(1)"
    CONSOLE_DROPDOWN_MENU = "#console-type-select .dropdown-menu"
    # Inline console
    INLINE_CONSOLE_TYPE = "Graphics Console (VNC)"
    INLINE_CONSOLE_FRAME_NAME = "vm-{}-novnc-frame-container"
    INLINE_CTRL_ALT_DEL_BUTTON = _ID_PREFIX + "vnc-ctrl-alt-del"
    INLINE_CANVAS = "#noVNC_canvas"
    # External console
    EXTERNAL_CONSOLE_NAME = "Graphics Console in Desktop Viewer"
    EXTERNAL_CONSOLE_SELECT_ITEM = "li[data-data='desktop']"
    LAUNCH_REMOTE_VIEWER_BUTTON = _ID_PREFIX + "consoles-launch"
    VV_FILE_ATTR = ("data:application/x-virt-viewer,%5Bvirt-viewer%5D%0Atype%3Dspice"
                    "%0Ahost%3D{}%0Aport%3D{}%0Adelete-this-file%3D1%0Afullscreen%3D0%0A")
    DYNAMICAL_FILE = "#dynamically-generated-file"
    MORE_INFO_LINK = ".machines-desktop-viewer-block a[href='#']"
    CONSOLE_MANUAL_ADDRESS = _ID_PREFIX + 'consoles-manual-address'
    CONSOLE_MANUAL_PORT = _ID_PREFIX + 'consoles-manual-port-{}'
    # serial console
    SERIAL_CONSOLE_NAME = "Serial Console"
    SERIAL_CONSOLE_SELECT_ITEM = "li[data-data='serial-browser']"
    SERIAL_CANVAS = "div.terminal canvas.xterm-text-layer"
    SERIAL_CONSOLE_DISCONNECT_BUTTON = "#{}-serialconsole-disconnect"
    SERIAL_CONSOLE_RECONNECT_BUTTON = "#{}-serialconsole-reconnect"

    # non root user operation alert
    ALERT_CLOSE_BUTTON = "div.alert-warning span.pficon-close"
    LAST_MESSAGE = _ID_PREFIX + 'last-message'
    RESTART_ALERT_TEXT = "VM REBOOT action failed"
    FORCE_RESTART_ALERT_TEXT = "VM FORCE REBOOT action failed"
    SHUTDOWN_ALERT_TEXT = "VM SHUT DOWN action failed"
    FORCE_SHUTDOWN_ALERT_TEXT = "VM FORCE OFF action failed"
    SEND_NMI_ALEART_TEXT = "VM SEND Non-Maskable Interrrupt action failed"
    DELETE_VM_ALEART_TEXT = ("error: failed to connect to the hypervisor "
                             "error: authentication "
                             "failed: access denied by policy")
    DELETE_VM_ALEART = "div.alert-danger.dialog-error span:nth-of-type(2)"

    def open_page(self):
        self.click(self.MACHINES_LINK)
        self.switch_to_frame(self.MACHINES_FRAME_NAME)
        # set static vm name
        self.vmname = "staticvm"

    def open_vm_row(self):
        self.click(self.VM_ROW.format(self.vmname))

    def open_usage_subtab(self):
        self.hover_and_click(self.USAGE_TAB.format(self.vmname))

    def open_disks_subtab(self, state='running'):
        self.hover_and_click(self.DISKS_TAB.format(self.vmname))
        if state == 'running':
            self.wait_invisible(self.DISKS_NOTIFICATION.format(self.vmname))

    def open_networks_subtab(self):
        self.hover_and_click(self.NETWORKS_TAB.format(self.vmname))

    def open_consoles_subtab(self):
        self.hover_and_click(self.CONSOLES_TAB.format(self.vmname))

    def run_vm_on_ui(self):
        self.click(self.RUN_BUTTON.format(self.vmname))

    def restart_vm_on_ui(self):
        self.hover_and_click(self.RESTART_BUTTON.format(self.vmname))

    def force_restart_vm_on_ui(self):
        self.click(self.RESTART_DROPDOWN_BUTTON.format(self.vmname))
        self.click(self.FORCE_RESTART_BUTTON.format(self.vmname))

    def shutdown_vm_on_ui(self):
        self.click(self.SHUTDOWN_BUTTON.format(self.vmname))

    def forceoff_vm_on_ui(self):
        self.click(self.SHUTDOWN_DROPDOWN_BUTTON.format(self.vmname))
        self.click(self.FORCEOFF_BUTTON.format(self.vmname))

    def sendnmi_vm_on_ui(self):
        self.click(self.SHUTDOWN_DROPDOWN_BUTTON.format(self.vmname))
        self.click(self.SENDNMI_BUTTON.format(self.vmname))

    def delete_vm_on_ui(self, del_storage=True):
        self.click(self.DELETE_BUTTON.format(self.vmname))
        if not del_storage:
            self.click(self.DELETE_STORAGE_CHECKBOX)
        self.click(self.DELETE_VM_BUTTON)

    def prepare_running_vm(self):
        state = self.get_vm_state_on_host()
        if not state:
            self.create_running_vm_by_virsh()
        if state == 'shut off':
            self.start_vm_by_virsh()

    def prepare_stop_vm(self):
        state = self.get_vm_state_on_host()
        if not state:
            self.create_stop_vm_by_virsh()
        if state == 'running':
            self.stop_vm_by_virsh()

    def prepare_no_vm(self):
        state = self.get_vm_state_on_host()
        if not state:
            return
        if state == 'running':
            self.destroy_vm_by_virsh()
        self.undefine_vm_by_virsh()

    def create_running_vm_by_virsh(self):
        """
        The vm.xml and vm.qcow2 should be copied to host beforehand,
        vm.qcow2 should be installed with OS.
        """
        self.create_stop_vm_by_virsh()
        cmd = 'virsh start {}'.format(self.vmname)
        self.host.execute(cmd)
        # wait for guest os to start up.
        sleep(self.WAIT_VM_UP)

    def create_stop_vm_by_virsh(self):
        cmd = 'virsh define /var/lib/libvirt/images/staticvm.xml'
        self.host.execute(cmd)

    def start_vm_by_virsh(self):
        cmd = 'virsh start {}'.format(self.vmname)
        self.host.execute(cmd)
        sleep(self.WAIT_VM_UP)

    def stop_vm_by_virsh(self):
        cmd = 'virsh shutdown {}'.format(self.vmname)
        self.host.execute(cmd)
        sleep(self.WATI_VM_DOWN)

    def destroy_vm_by_virsh(self):
        cmd = 'virsh destroy {}'.format(self.vmname)
        self.host.execute(cmd)

    def undefine_vm_by_virsh(self):
        cmd = 'virsh undefine {}'.format(self.vmname)
        self.host.execute(cmd)

    def get_no_vm_text_on_ui(self):
        return self.get_text(self.NO_VM_EL)

    def get_vm_list_on_host(self):
        cmd = 'virsh list --all --name'
        ret = self.host.execute(cmd)
        vm_list = []
        for line in ret.split('\n'):
            vm_list.append(line.strip(' '))
        return vm_list

    def get_dumpxml_on_host(self):
        cmd = 'virsh dumpxml {}'.format(self.vmname)
        ret = self.host.execute(cmd)
        self.vm_xml_info = xmltodict.parse(ret)

    def get_vm_state_on_host(self):
        cmd = 'virsh domstate {}'.format(self.vmname)
        try:
            ret = self.host.execute(cmd)
            return ret.split('\n')[0]
        except RunCmdError:
            return None

    def get_vm_state_on_ui(self):
        return self.get_text(self.VM_STATE.format(self.vmname))

    def get_autostart_state_on_host(self):
        cmd = 'virsh dominfo {} | grep -i autostart'.format(self.vmname)
        ret = self.host.execute(cmd)
        return ret.split(' ')[-1]

    def get_overview_info_in_xml(self, key):
        if key == 'memory':
            value = int(self.vm_xml_info['domain']
                        ['memory']['#text']) / (1024 * 1024)
        if key == 'vcpus-count':
            value = self.vm_xml_info['domain']['vcpu']['#text']
        if key == 'cputype':
            mode = self.vm_xml_info['domain']['cpu']['@mode']
            model = self.vm_xml_info['domain']['cpu']['model']['#text']
            value = mode + " (" + model + ")"
        if key == 'emulatedmachine':
            value = self.vm_xml_info['domain']['os']['type']['@machine']
        if key == 'bootorder':
            value_list = []
            boot_list = self.vm_xml_info['domain']['os']['boot']
            if not isinstance(boot_list, list):
                boot_list = [boot_list]
            for boot in boot_list:
                dev = boot['@dev']
                if dev == 'hd':
                    dev = 'disk'
                value_list.append(dev)
            value = ','.join(value_list)
        if key == 'autostart':
            value = self.get_autostart_state_on_host() + 'd'
        return value

    def get_overview_info_on_ui(self, key):
        el_descriptor = self._ID_PREFIX.format(self.vmname) + key
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
        disk = self.DISK_COLUMN_TEMPLATE.format(self.vmname, target)
        if column == 'readonly':
            el_descriptor = self.DISK_COLUMN_READONLY.format(disk.lstrip('#'))
        elif column == 'source':
            el_descriptor = self.DISK_COLUMN_SOURCE.format(disk)
        else:
            el_descriptor = disk + column
        return self.get_text(el_descriptor)

    def get_disk_count_on_ui(self):
        return self.get_text(self.DISKS_COUNT.format(self.vmname))

    def get_network_list_in_xml(self):
        value = []
        ret = self.vm_xml_info['domain']['devices']['interface']
        if not isinstance(ret, list):
            value.append(ret)
        else:
            value = ret
        return value

    def get_network_state_on_host(self, interface):
        cmd = 'virsh domif-getlink {} {}'.format(self.vmname, interface)
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
        column_template = self.NETWORK_COLUMN_TEMPLATE.format(
            self.vmname, seq_num)
        if column in ['source', 'state', 'button']:
            parent = column
            son = 'span'
            if column == 'button':
                parent = 'state'
                son = 'button'
            parent_id = column_template + parent
            el_descriptor = "{} {}".format(parent_id, son)
        else:
            el_descriptor = column_template + column
        return self.get_text(el_descriptor)

    def get_network1_state_on_ui(self):
        return self.get_text(self.NETWORK1_STATE.format(self.vmname))

    def get_network1_plug_button_text(self):
        return self.get_text(self.NETWORK1_PLUG_BUTTON.format(self.vmname))

    def click_network1_plug_button(self):
        current_text = self.get_network1_plug_button_text()
        if current_text == "Unplug":
            expected_text = "Plug"
        else:
            expected_text = "Unplug"
        self.click(self.NETWORK1_PLUG_BUTTON.format(self.vmname))
        self.wait_in_text(self.NETWORK1_PLUG_BUTTON.format(
            self.vmname), expected_text)

    def prepare_network1_plug_button(self, expected_text):
        plug_text = self.get_network1_plug_button_text()
        if plug_text != expected_text:
            self.click_network1_plug_button()

    def get_network1_state_on_host(self):
        target = self.get_text(self.NETWORK1_TARGET.format(self.vmname))
        return self.get_network_state_on_host(target)

    def get_memory_usage_on_ui(self, state='off'):
        if state == 'running':
            for count in range(0, 5):
                value = self.get_text(self.USED_MEMORY_VALUE)
                if value != '0.00':
                    break
                sleep(1)
        else:
            value = self.get_text(self.USED_MEMORY_VALUE)
        unit = self.get_text(self.USED_MEMORY_UNIT)
        return value + unit

    def get_cpu_usage_on_ui(self, state='off'):
        if state == 'running':
            for count in range(0, 15):
                value = self.get_text(self.USED_CPU_VALUE)
                if value != '0.0':
                    break
                sleep(1)
        else:
            value = self.get_text(self.USED_CPU_VALUE)
        unit = self.get_text(self.USED_CPU_UNIT)
        return value + unit

    def _switch_back_to_main_frame(self):
        self.switch_to_default_content()
        self.switch_to_frame(self.MACHINES_FRAME_NAME)

    def _select_console_menu(self, console_item):
        self._switch_back_to_main_frame()
        self.click(self.CONSOLE_TYPE_BUTTON)
        self.hover_and_click(console_item)
        self.wait_invisible(self.CONSOLE_DROPDOWN_MENU)

    def get_console_type(self):
        return self.get_text(self.CONSOLE_TYPE_TEXT)

    # inline console
    def send_ctrl_alt_del(self):
        self._switch_back_to_main_frame()
        self.hover_and_click(
            self.INLINE_CTRL_ALT_DEL_BUTTON.format(self.vmname))

    def wait_canvas_change(self):
        def wait(expected_width):
            for count in range(0, 20):
                width = self.get_attribute(self.INLINE_CANVAS, 'width')
                if width == expected_width:
                    break
                sleep(1)
            else:
                return False
            return True
        self.switch_to_frame(
            self.INLINE_CONSOLE_FRAME_NAME.format(self.vmname))
        if not wait('720'):
            return False
        if not wait('1024'):
            return False
        return True

    # external console
    def open_external_console_page(self):
        self._select_console_menu(self.EXTERNAL_CONSOLE_SELECT_ITEM)

    def get_external_console_info_in_xml(self):
        self.get_dumpxml_on_host()
        viewer_list = []
        graphic_list = self.vm_xml_info['domain']['devices']['graphics']
        if not isinstance(graphic_list, list):
            viewer_list.append(graphic_list)
        else:
            viewer_list = graphic_list
        viewer_info_list = []
        for viewer in viewer_list:
            viewer_info = {}
            viewer_info['type'] = viewer['@type']
            viewer_info['port'] = viewer['@port']
            viewer_info['ip'] = viewer['@listen']
            viewer_info_list.append(viewer_info)
        return viewer_info_list

    def get_external_console_info_in_vv(self):
        return self.get_attribute(self.DYNAMICAL_FILE, 'href')

    def launch_remote_viewer(self):
        self.click(self.LAUNCH_REMOTE_VIEWER_BUTTON.format(self.vmname))

    def toggle_more_info(self):
        self.click(self.MORE_INFO_LINK)

    def get_consoles_manual_address_on_ui(self):
        return self.get_text(self.CONSOLE_MANUAL_ADDRESS.format(self.vmname))

    def get_consoles_manual_port_on_ui(self, con_type):
        return self.get_text(self.CONSOLE_MANUAL_PORT.format(self.vmname, con_type))

    # serial console
    def open_serial_console_page(self):
        self._select_console_menu(self.SERIAL_CONSOLE_SELECT_ITEM)

    def disconnect_serial_console(self):
        self._switch_back_to_main_frame()
        self.click(self.SERIAL_CONSOLE_DISCONNECT_BUTTON.format(self.vmname))
        sleep(1)

    def reconnect_serial_console(self):
        self._switch_back_to_main_frame()
        self.click(self.SERIAL_CONSOLE_RECONNECT_BUTTON.format(self.vmname))
        sleep(1)

    def login_non_root_user(self):
        cmd = 'echo redhat | passwd --stdin test'
        self.host.execute(cmd)
        self.logout()
        self.login('test', 'redhat')

    def get_last_message_text(self):
        value = self.get_text(self.LAST_MESSAGE.format(self.vmname))
        self.click(self.ALERT_CLOSE_BUTTON)
        return value

    def get_delete_vm_alert_text(self):
        return self.get_text(self.DELETE_VM_ALEART)

    def open_vcpu_details_window(self):
        self.click(self.VCPU_DETAILS_LINK.format(self.vmname))

    def set_vcpu_details(self, maxnum, count, sockets, cores, threads):
        self.input_text(self.VCPU_MAXIMUM_INPUT, maxnum, control=True)
        self.input_text(self.VCPU_COUNT_INPUT, count, control=True)
        self.click(self.VCPU_SOCKETS_SELECT_BUTTON)
        self.click(self.VCPU_SOCKETS_ITEM.format(sockets))
        self.click(self.VCPU_CORES_SELECT_BUTTON)
        self.click(self.VCPU_CORES_ITEM.format(cores))
        self.click(self.VCPU_THREADS_SELECT_BUTTON)
        self.click(self.VCPU_THREADS_ITEM.format(threads))
        self.click(self.VCPU_APPLY_BUTTON)

    def get_vcpu_count_on_ui(self):
        return self.get_text(self.VCPU_DETAILS_LINK.format(self.vmname))

    def get_vcpu_topology_in_xml(self):
        self.get_dumpxml_on_host()
        cpu_topo = self.vm_xml_info['domain']['cpu']['topology']
        value = []
        for i in ['@sockets', '@cores', '@threads']:
            value.append(cpu_topo[i])
        return value
