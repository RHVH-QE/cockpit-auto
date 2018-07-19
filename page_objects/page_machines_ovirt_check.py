import os
import yaml
import xmltodict
from time import sleep
from seleniumlib import SeleniumTest
from utils.machine import RunCmdError
from utils.rhvmapi import RhevmAction

class MachinesOvirtCheckPage(SeleniumTest):
    """
    :avocado: disable
    """
    WAIT_VM_UP = 10
    WATI_VM_DOWN = 5
    WAIT_VM_SUSPEND = 15

    VM_NAME = "HostedEngine"
    TEMPLATE = "Blank"

    # Host Page
    MACHINES_OVIRT_LINK = "#sidebar-menu a[href='/machines']"
    MACHINES_OVIRT_FRAME_NAME = "/machines"

    LOCALHOST_BUTTON = "#host-nav-link"

    ENGINE_USERNAME = "//input[@name='username']"
    ENGINE_PASSWD = "//input[@name='password']"
    LOGININ_BUTTON = "//button[@type='submit']"

    INPUT_FQDN = "//input[@placeholder='engine.mydomain.com']"
    INPUT_PORT = "//input[@placeholder='443']"
    REGISTER_OVIRT_BUTTON = "//button[text()='Register oVirt']"

    OK_BUTTON = "//button[text()='OK']"
    OVIRT_HOST_STATUS = ".ovirt-host-status-label"
    HOST_TO_MAINTENANCE = "#ovirt-host-to-maintenance"
    CREATE_NEW_VM = "//div[text()='Create New VM']"
    CREATE_NEW_VM_INFO = ".tooltip-inner"

    # id prefix, {} should be the actual vm name
    _ID_PREFIX = "#vm-{}-".format(VM_NAME)
    VM_ROW = _ID_PREFIX + 'row'
    VM_STATE = _ID_PREFIX + 'state'
    RUN_BUTTON = _ID_PREFIX + 'run'
    RESTART_BUTTON = _ID_PREFIX + 'reboot'
    BUTTON_WARN = "#vm-{}-last-message".format(VM_NAME)
    SHUTDOWN_BUTTON = _ID_PREFIX + 'off'
    RESTART_DROPDOWN_BUTTON = RESTART_BUTTON + '-caret'
    SHUTDOWN_DROPDOWN_BUTTON = SHUTDOWN_BUTTON + '-caret'
    FORCERESTART_BUTTON = _ID_PREFIX + 'forceReboot'
    FORCEOFF_BUTTON = _ID_PREFIX + 'forceOff'
    SENDNMI_BUTTON = _ID_PREFIX + 'sendNMI'
    SUSPEND_BUTTON = _ID_PREFIX + 'ovirt-suspendbutton'

    #DELETE_BUTTON = _ID_PREFIX + 'delete'
    #DELETE_STORAGE_CHECKBOX = "input[type=checkbox]"
    #DELETE_VM_BUTTON = "#cockpit_modal_dialog .modal-footer button:nth-of-type(2)"

    # overview subtab
    OVERVIEW_INFO_NAMES = ['memory', 'vcpus',
                           'cputype', 'emulatedmachine', 'bootorder', 'autostart',
                           'ovirt-description', 'ovirt-fqdn', 'ovirt-starttime']

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
    DISK_COLUMN_NAMES = ['device', 'target', 'bus', 'readonly', 'source'] # 'used', 'capacity' not list here
    DISK_COLUMN_READONLY = "//*[@id='{}bus']//parent::*//following-sibling::*"
    #DISK_COLUMN_SOURCE = "{}source .machines-disks-source-value"
    DISK_COLUMN_SOURCE = "{}source .machines-disks-source-value"

    # networks subtab
    NETWORKS_TAB = _ID_PREFIX + "networks"
    NETWORK_COLUMN_TEMPLATE = _ID_PREFIX + "network" + "-{}-"
    NETWORK_COLUMN_NAMES = ['type', 'model',
                            'mac', 'target', 'source', 'state']
    NETWORK1_PLUG_BUTTON = "#vm-{}-network-1-state button".format(VM_NAME)
    PLUG_WARNING = ".machines-status-alert"


    # ovirt subtab
    _OVIRT_TEMPLATE = "//td[@id='vm-{}-{}']"
    OVIRT_TAB = _ID_PREFIX + "ovirt"
    OVIRT_INFO_NAMES = ['ovirt-description', 'ovirt-template', 'ovirt-ostype',
                        'ovirt-ha', 'ovirt-stateless', 'ovirt-optimizedfor']

    MIGRATE_VM_BUTTON = "#vm-{}-ovirt-migratetobutton".format(VM_NAME)
    CONFIRM_MIGRATE = "//button[text()='Confirm migration']"

    _TOPNAV_TEMPLATE = "#ovirt-topnav-{}"
    # Cluster Page
    CLUSTER_TOPNAV = _TOPNAV_TEMPLATE.format('clustervms')
    CLUSTER_VM_NAME = "tbody>tr>th"
    CLUSTER_VM_DESCRIPTION = "tbody>tr>td:nth-of-type(2)>span"
    CLUSTER_VM_TEMPLATE = "tbody>tr>td:nth-of-type(3)>span"
    CLUSTER_VM_MEMORY = "tbody>tr>td:nth-of-type(4)>div"
    CLUSTER_VM_VCPU = "tbody>tr>td:nth-of-type(5)>span"
    CLUSTER_VM_OS = "tbody>tr>td:nth-of-type(6)>div"
    CLUSTER_VM_HA = "tbody>tr>td:nth-of-type(7)>div"
    CLUSTER_VM_STATELESS = "tbody>tr>td:nth-of-type(8)>div"
    CLUSTER_HOST_LINK = "tbody>tr>td:nth-of-type(9)>a"
    CLUSTER_VM_ACTION = "tbody>tr>td:nth-of-type(10)"
    CLUSTER_VM_STATE = "tbody>tr>td:nth-of-type(11)>span>span"

    CLUSTER_INFO_NAME = ['name', 'description', 'template', 'memory',
                        'vcpus', 'os', 'ha', 'stateless', 'action', 'state']

    # Templates Page
    TEMPLATES_TOPNAV = _TOPNAV_TEMPLATE.format('clustertemplates')
    TEMPLATE_INFO_NAME = ['name', 'version', 'base-template', 'description',
                            'memory', 'vcpus', 'os', 'ha', 'stateless']
    TEMPLATE_NAME = "tbody>tr>th"
    TEMPLATE_VERSION = "tbody>tr>td:nth-of-type(2)"
    TEMPLATE_BASE = "tbody>tr>td:nth-of-type(3)"
    TEMPLATE_DESCRIPTION = "tbody>tr>td:nth-of-type(4)>span"
    TEMPLATE_MEMORY = "tbody>tr>td:nth-of-type(5)>div"
    TEMPLATE_VCPUS = "tbody>tr>td:nth-of-type(6)>span"
    TEMPLATE_OS = "tbody>tr>td:nth-of-type(7)>div"
    TEMPLATE_HA = "tbody>tr>td:nth-of-type(8)>div"
    TEMPLATE_STATELESS = "tbody>tr>td:nth-of-type(9)>div"
    TEMPLATE_ACTION = "tbody>tr>td:nth-of-type(10)>span>button"

    TEMPLATE_NEW_VM = "//input[@placeholder='Enter New VM name']"
    CREATE_NEW_VM_BUTTON = "//button[text()='Create']"
    CREATE_NEW_VM_ERROR = "#clustervm-Blank-actionerror"

    # VDSM Page
    VDSM_TOPNAV = _TOPNAV_TEMPLATE.format('vdsm')
    VDSM_TEXTAREA = ".ovirt-provider-vdsm-editor"
    VDSM_SAVE_BUTTON = "//button[text()='Save']"
    VDSM_SAVE_OK = "//button[text()='OK']"
    VDSM_SERVICE_LINK = "//a[text()='VDSM Service Management']"
    VDSM_RELOAD_BUTTON = "//button[text()='Reload']"

    def open_page(self):
        a = self.get_data('machines_ovirt.yml')
        self.config_dict = yaml.load(open(a))

        self.rhvm = RhevmAction(self.config_dict['fqdn'], self.config_dict['username'],
                                 self.config_dict['passwd'])
        self.click(self.LOCALHOST_BUTTON)
        self.click(self.MACHINES_OVIRT_LINK)
        self.switch_to_frame(self.MACHINES_OVIRT_FRAME_NAME)

        test_cmd = "test -f /etc/cockpit/machines-ovirt.config"
        if not self.host.execute(test_cmd, raise_exception=False).succeeded:
            self.assert_element_visible(self.REGISTER_OVIRT_BUTTON)
            self.input_text(self.INPUT_FQDN, self.config_dict['fqdn'])
            self.input_text(self.INPUT_PORT, self.config_dict['port'])
            self.click(self.REGISTER_OVIRT_BUTTON)

        sleep(5)
        self.driver.get(self.get_current_url())
        self.input_text(self.ENGINE_USERNAME, self.config_dict['username'])
        self.input_text(self.ENGINE_PASSWD, self.config_dict['passwd'])
        self.click(self.LOGININ_BUTTON)
        sleep(5)

        self.driver.get(self.get_current_url())
        self.switch_to_frame(self.MACHINES_OVIRT_FRAME_NAME)
        self.assert_element_visible(self.OVIRT_HOST_STATUS)

    def disable_create_new_vm(self):
        self.click(self.CREATE_NEW_VM)
        self.assert_element_visible(self.CREATE_NEW_VM_INFO)

    def host_to_maintenance(self):
        i = 0
        self.click(self.HOST_TO_MAINTENANCE)
        self.click(self.OK_BUTTON)
        while True:
            if i > 50:
                raise RuntimeError("Timeout waitting for host to maintenance")
            host_status = self.rhvm.get_host_status(self.config_dict['first_host_name'])

            if host_status == 'maintenance':
                return True
            sleep(10)
            i += 1

    def open_vm_row(self):
        self.click(self.VM_ROW)

    def open_usage_subtab(self):
        self.hover_and_click(self.USAGE_TAB)

    def open_disks_subtab(self):
        self.hover_and_click(self.DISKS_TAB)
        sleep(2)

    def open_networks_subtab(self):
        self.hover_and_click(self.NETWORKS_TAB)

    def open_consoles_subtub(self):
        pass

    def open_ovirt_subtub(self):
        self.hover_and_click(self.OVIRT_TAB)

    def run_ovirt_vm_on_ui(self):
        self.click(self.RUN_BUTTON)

    def reboot_he_vm_on_ui(self):
        self.click(self.RESTART_BUTTON)
        sleep(self.WATI_VM_DOWN)
        #sleep(self.WAIT_VM_UP)
        self.assert_element_visible(self.BUTTON_WARN)
        warn_text = self.get_text(self.BUTTON_WARN)
        self.assertEqual(warn_text, 'REBOOT action failed')

    def reboot_ovirt_vm_on_ui(self):
        self.click(self.RESTART_BUTTON)
        sleep(self.WATI_VM_DOWN)

    def force_reboot_he_vm_on_ui(self):
        self.click(self.RESTART_DROPDOWN_BUTTON)
        self.click(self.FORCERESTART_BUTTON)
        sleep(self.WATI_VM_DOWN)
        #sleep(self.WAIT_VM_UP)
        self.assert_element_visible(self.BUTTON_WARN)
        warn_text = self.get_text(self.BUTTON_WARN)
        self.assertEqual(warn_text, 'REBOOT action failed')

    def force_reboot_ovirt_vm_on_ui(self):
        self.click(self.RESTART_DROPDOWN_BUTTON)
        self.click(self.FORCERESTART_BUTTON)
        sleep(self.WATI_VM_DOWN)

    def shutdown_he_vm_on_ui(self):
        self.click(self.SHUTDOWN_BUTTON)
        sleep(self.WATI_VM_DOWN)
        self.assert_element_visible(self.BUTTON_WARN)
        warn_text = self.get_text(self.BUTTON_WARN)
        self.assertEqual(warn_text, 'SHUTDOWN action failed')

    def shutdown_ovirt_vm_on_ui(self):
        self.click(self.SHUTDOWN_BUTTON)
        sleep(self.WATI_VM_DOWN)

    def forceoff_he_vm_on_ui(self):
        self.click(self.SHUTDOWN_DROPDOWN_BUTTON)
        self.click(self.FORCEOFF_BUTTON)
        sleep(self.WATI_VM_DOWN)
        self.assert_element_visible(self.BUTTON_WARN)
        warn_text = self.get_text(self.BUTTON_WARN)
        self.assertEqual(warn_text, 'SHUTDOWN action failed')

    def forceoff_ovirt_vm_on_ui(self):
        self.click(self.SHUTDOWN_DROPDOWN_BUTTON)
        self.click(self.FORCEOFF_BUTTON)
        sleep(self.WATI_VM_DOWN)

    def sendnmi_vm_on_ui(self):
        self.click(self.SHUTDOWN_DROPDOWN_BUTTON)
        self.click(self.SENDNMI_BUTTON)
        self.assert_element_visible(self.BUTTON_WARN)

    def suspend_he_vm_on_ui(self):
        # TODO
        # When supend the HE-VM , it is a bad request from the console, because 
        # the HE-VM is not managed by engine, but now the UI don't pop any warnings.
        pass

    def suspend_ovirt_vm_on_ui(self):
        self.click(self.SUSPEND_BUTTON)
        i = 0
        while True:
            if i > 20:
                raise RuntimeError("Timeout for waiting for the vm to supend status")
            vm_status = self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['vm-status']

            if vm_status == 'supend':
                return True
            sleep(10)
            i += 1

    def remove_libvirt_auth(self):
        '''
        If remove the libvirt auth, the vdsm auth will fail, then the vm will be down,
        so this method cannot be used.
        '''
        remove_cmd = "sed -i '/auth_unix_rw/'d /etc/libvirt/libvirtd.conf"
        self.host.execute(remove_cmd, raise_exception=False)
        self.host.execute("systemctl restart libvirtd", raise_exception=False)

    def get_dumpxml_on_host(self):
        false, true = False, True
        cmd = 'vdsm-client Host getVMFullList vmName={} > /root/info.txt'.format(self.VM_NAME)
        self.host.execute(cmd)

        self.host.get_file("/root/info.txt", "info.txt")
        fp = open("info.txt",'rw+')

        vm_info_list = eval(fp.read())
        for i in range(0, len(vm_info_list)):
            if vm_info_list[i]['vmName'] == self.VM_NAME:
                self.dict_info = vm_info_list[i]
        return self.dict_info

    def get_vmxml_on_host(self):
        self.vm_xml_info = xmltodict.parse(self.get_dumpxml_on_host()['xml'])
        return self.vm_xml_info

    def get_vm_state_on_host(self):
        info = self.get_dumpxml_on_host()
        if info['status'] == 'Up':
            state = 'running'
        else:
            state = 'shut off'
        return state

    def get_vm_state_on_ui(self):
        return self.get_text(self.VM_STATE)

    def get_autostart_state_on_host(self):
        pass

    def get_vm_description(self):
        return self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['ovirt-description']

    def get_overview_info_in_xml(self, key):
        if key == 'memory':
            value = int(self.dict_info['guestNumaNodes'][0]['memory']) / 1024 + 1
        if key == 'vcpus':
            value = len([i for i in self.dict_info['guestNumaNodes'][0]['cpus'].split(',')])
        if key == 'cputype':
            value = "custom (" + self.dict_info['cpuType'] + ")"
        if key == 'emulatedmachine':
            value = self.dict_info['emulatedMachine']
        if key == 'bootorder':
            value = 'disk' # This is hard code, should modify the value from xml
        if key == 'autostart':
            value = 'disabled'  # This is hard code, should modify the value from xml
        if key == 'ovirt-description':
            value = self.get_vm_description()
        if key == 'ovirt-fqdn':
            value = self.config_dict['fqdn']
        if key == 'ovirt-starttime':
            value = ''  # Here is a bug
        return value

    def get_overview_info_on_ui(self, key):
        el_descriptor = self._ID_PREFIX + key
        value = self.get_text(el_descriptor)
        if key == 'memory':
            value = int(value.split(' ')[0].split('.')[0])
        if key == 'vcpus':
            value = int(value)
        if key == 'bootorder':
            value = str(value)

        return value

    def get_memory_usage_on_ui(self):
        value = self.get_text(self.USED_MEMORY_VALUE)
        unit = self.get_text(self.USED_MEMORY_UNIT)
        return value + unit

    def get_cpu_usage_on_ui(self):
        value = self.get_text(self.USED_CPU_VALUE)
        unit = self.get_text(self.USED_CPU_UNIT)
        return value + unit

    def get_disk_list_in_xml(self):
        value = []
        for i in range(0, len(self.dict_info['devices'])):
            if self.dict_info['devices'][i]['type'] == 'disk':
                value.append(self.dict_info['devices'][i])

        return value

    def get_disk_info_in_xml(self, disk, key):
        # disk is a dict , include the whole disk information
        if key == 'device':
            value = disk['device']
        if key == 'target':
            value = disk['name']
        if key == 'bus':
            value = disk['iface']
        # The "used" and "capacity" is not listed
        if key == 'readonly':
            if disk['readonly'] == 'False':
                value = 'no'
            else:
                value = 'yes'
        if key == 'source':
            value = disk['path']
        return value

    def get_disk_info_on_ui(self, target, column):
        disk = self.DISK_COLUMN_TEMPLATE.format(target)
        if column == 'readonly':
            el_descriptor = self.DISK_COLUMN_READONLY.format(disk.lstrip('#'))
        elif column == 'source':
            el_descriptor = self.DISK_COLUMN_SOURCE.format(disk)
            try:
                source = self.get_text(el_descriptor)
            except Exception as e:
                return ''
            else:
                return source
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

    def get_network_state_on_host(self):
        return self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['vm-status']

    def get_network_info_in_xml(self, network, key):
        # network is a xmltodict object
        if key == 'type':
            value = network['@type']
        if key == 'model':
            value = network['model']['@type']
        if key == 'mac':
            value = network['mac']['@address']
        if key == 'target':
            #value = network['target']['@dev']
            value = 'vnet0' # Hard Code
        if key == 'source':
            net_type = '@' + network['@type']
            value = network['source'][net_type]
        if key == 'state':
            #value = network['link']['@state']
            value = self.get_network_state_on_host()
        if key == 'button':
            #state = network['link']['@state']
            state = self.get_network_state_on_host()
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

    def get_ovirt_info_on_host(self, key):
        if key == 'ovirt-ha':
            if self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)[key] == 'false':
                return 'disabled'
            else:
                return 'enabled'
        if key == 'ovirt-stateless':
            if self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)[key] == 'false':
                return 'no'
            else:
                return 'yes'
        if key == 'ovirt-template':
            return 'Blank' # Hard Code
        return self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)[key]

    def get_ovirt_info_on_ui(self, key):
        # The css selector is not useful here. 
        # el_descriptor = self._ID_PREFIX + key
        el_descriptor = self._OVIRT_TEMPLATE.format(self.VM_NAME, key)
        value = self.get_text(el_descriptor)
        return value

    def migrate_vm_to_additional_host(self):
        vm_on_first_host = self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['test']
        self.click(self.MIGRATE_VM_BUTTON)
        self.click(self.CONFIRM_MIGRATE)
        i = 0
        while True:
            if i > 50:
                raise RuntimeError("Migrate the HostedEngine VM to another Host failed")
            vm_on_second_host = self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['host_id']

            if vm_on_first_host != vm_on_second_host:
                return True
            sleep(10)
            i += 1

    # Check the Cluster Page
    def get_cluster_info_in_xml(self, key):
        if key == 'memory':
            value = int(self.dict_info['guestNumaNodes'][0]['memory']) / 1024 + 1
        if key == 'vcpus':
            value = len([i for i in self.dict_info['guestNumaNodes'][0]['cpus'].split(',')])
        if key == 'os':
            value = self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['ovirt-ostype']
        if key == 'template':
            value = 'Blank'
        if key == 'description':
            value = self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['ovirt-description']
        if key == 'name':
            value = self.VM_NAME
        if key == 'ha':
            value = self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['ovirt-ha']
        if key == 'stateless':
            value = self.rhvm.get_vm_ovirt_info_on_engine(self.VM_NAME)['ovirt-stateless']
        if key == 'state':
            value = self.get_vm_state_on_host()
        if key == 'action':
            value = ''
        # exclude the "host" key
        return value

    def get_cluster_info_in_ui(self, key):
        if key == 'memory':
            value = int(self.get_text(self.CLUSTER_VM_MEMORY).split(' ')[0].split('.')[0])
        if key == 'vcpus':
            value = int(self.get_text(self.CLUSTER_VM_VCPU))
        if key == 'os':
            value = self.get_text(self.CLUSTER_VM_OS)
        if key == 'template':
            value = self.get_text(self.CLUSTER_VM_TEMPLATE)
        if key == 'description':
            value = self.get_text(self.CLUSTER_VM_DESCRIPTION)
        if key == 'name':
            value = self.get_text(self.CLUSTER_VM_NAME)
        if key == 'ha':
            value = self.get_text(self.CLUSTER_VM_HA)
            if value == 'no':
                value = 'false'
            else:
                value = 'true'
        if key == 'stateless':
            value = self.get_text(self.CLUSTER_VM_STATELESS)
            if value == 'no':
                value = 'false'
            else:
                value = 'true'
        if key == 'state':
            value = self.get_text(self.CLUSTER_VM_STATE)
        if key == 'action':
            value = self.get_text(self.CLUSTER_VM_ACTION)
        # exclude the "host" key
        return value

    def click_cluster_host_link(self):
        host_name = self.get_text(self.CLUSTER_HOST_LINK)
        sleep(2)
        self.click(self.CLUSTER_HOST_LINK)
        link = self.get_current_url()
        sleep(5)
        if link != 'https://{}:9090/machines'.format(host_name):
            self.fail()

    # Check the Templates Page
    def get_template_info_on_host(self, key):
        value = self.rhvm.get_template_info_on_engine(self.TEMPLATE)[key]
        return value

    def get_template_info_in_ui(self, key):
        if key == 'name':
            value = self.get_text(self.TEMPLATE_NAME)
        if key == 'version':
            value = self.get_text(self.TEMPLATE_VERSION)
        if key == 'base-template':
            value = self.get_text(self.TEMPLATE_BASE)
            if value == 'Blank':
                value = '00000000-0000-0000-0000-000000000000'
            else:
                value = '00000000-0000-0000-0000-000000000001' # Hard Code
        if key == 'description':
            value = self.get_text(self.TEMPLATE_DESCRIPTION)
        if key == 'memory':
            value = str(int(self.get_text(self.TEMPLATE_MEMORY).split(' ')[0])*1024*1024*1024)
        if key == 'vcpus':
            value = self.get_text(self.TEMPLATE_VCPUS)
        if key == 'os':
            value = self.get_text(self.TEMPLATE_OS)
        if key == 'stateless':
            value = self.get_text(self.TEMPLATE_STATELESS)
            if value == 'no':
                value = 'false'
            else:
                value = 'true'
        if key == 'ha':
            value = self.get_text(self.TEMPLATE_HA)
            if value == 'no':
                value = 'false'
            else:
                value = 'true'
        return value

    def create_vm_by_template(self):
        self.click(self.TEMPLATE_ACTION)
        self.input_text(self.TEMPLATE_NEW_VM, self.config_dict['new_vm'])
        self.click(self.CREATE_NEW_VM_BUTTON)
        sleep(2)
        self.click(self.CLUSTER_TOPNAV)
        sleep(10)

        new_vm_name = self.rhvm.list_vm(self.config_dict['new_vm'])
        if not new_vm_name:
            self.fail()

    def check_create_vm_twice(self):
        self.click(self.TEMPLATE_ACTION)
        self.input_text(self.TEMPLATE_NEW_VM, self.config_dict['new_vm'])
        self.click(self.CREATE_NEW_VM_BUTTON)
        sleep(2)
        self.assert_element_visible(self.CREATE_NEW_VM_ERROR)

    # Check the VDSM Page
    def get_vdsm_conf_file(self):
        try:
            self.host.get_file("/etc/vdsm/vdsm.conf", "vdsm.conf")
            fp = open('vdsm.conf', 'r+').read()
        except RunCmdError:
            return None
        return fp

    def check_vdsm_conf_in_ui(self):
        self.click(self.VDSM_TOPNAV)
        ret1 = self.get_vdsm_conf_file()
        ret2 = self.get_attribute(self.VDSM_TEXTAREA, "value")

        if ret1 != ret2:
            self.fail()

    def check_save_vdsm_conf_in_ui(self):
        fp = self.get_data("vdsm.conf.template1")
        content = open(fp, 'r+').read()
        self.click(self.VDSM_TOPNAV)
        self.input_text(self.VDSM_TEXTAREA, content)
        self.click(self.VDSM_SAVE_BUTTON)
        self.click(self.VDSM_SAVE_OK)

        ret = self.get_vdsm_conf_file()
        if ret != content:
            self.fail()

    def click_vdsm_service_mgmt(self):
        self.click(self.VDSM_TOPNAV)
        self.click(self.VDSM_SERVICE_LINK)
        sleep(10)
        link = self.get_current_url()
        if link != 'https://{}:9090/system/services#/vdsmd.service'.format(self.config_dict['host_ip']):
            self.fail()

    def check_reload_vdsm_conf_in_ui(self):
        fp = self.get_data("vdsm.conf.template2")
        content = open(fp, 'r+').read()
        self.click(self.VDSM_TOPNAV)
        prev_value = self.get_attribute(self.VDSM_TEXTAREA, "value")
        self.input_text(self.VDSM_TEXTAREA, content)
        self.click(self.VDSM_RELOAD_BUTTON)
        self.click(self.VDSM_SAVE_OK)
        sleep(2)

        next_value = self.get_attribute(self.VDSM_TEXTAREA, "value")

        if prev_value != next_value:
            self.fail()
