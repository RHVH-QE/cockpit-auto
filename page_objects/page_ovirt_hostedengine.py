import os
import yaml
import time
import simplejson
import urllib2
from seleniumlib import SeleniumTest
from utils.htmlparser import MyHTMLParser
from utils.machine import Machine
from utils.rhvmapi import RhevmAction


class OvirtHostedEnginePage(SeleniumTest):
    """
    :avocado: disable
    """

    OVIRT_HOSTEDENGINE_FRAME_NAME = "/ovirt-dashboard"
    HOSTEDENGINE_LINK = "//a[@href='#/he']"

    # Start button
    HE_START = "//span[@class='deployment-option-panel-container']/button[text()='Start']"

    # Guide Links
    GETTING_START_LINK = "//a[contains(text(), 'Installation Guide')]"
    MORE_INFORMATION_LINK = "//a[contains(text(), 'oVirt Homepage')]"

    # VM STAGE
    _TITLE = "//input[@title='%s']"
    _PLACEHOLDER = "//input[@placeholder='%s']"
    VM_FQDN = _PLACEHOLDER % 'ovirt-engine.example.com'
    MAC_ADDRESS = _TITLE % 'Enter the MAC address for the VM.'
    ROOT_PASS = "//label[text()='Root Password']//parent::*//input[@type='password']"
    VM_ADVANCED = "//a[text()='Advanced']"

    # TODO
    _DROPDOWN_MENU = "//label[text()='%s']//parent::*//button[contains(@class, 'dropdown-toggle')]"
    NETWORK_DROPDOWN = _DROPDOWN_MENU % 'Network Configuration'
    # TODO
    # BRIDGE_DROPDOWN
    SSH_ACCESS_DROPDOWN = _DROPDOWN_MENU % 'Root SSH Access'
    _DROPDOWN_VALUE = "//ul[@class='dropdown-menu']/li[@value='%s']"
    NETWORK_DHCP = _DROPDOWN_VALUE % 'dhcp'

    NETWORK_STATIC = _DROPDOWN_VALUE % 'static'
    VM_IP = _PLACEHOLDER % '192.168.1.2'
    IP_PREFIX = _PLACEHOLDER % '24'
    DNS_SERVER = "//div[contains(@class, 'multi-row-text-box-input')]" \
        "/input[@type='text']"

    # ENGINE STAGE
    ADMIN_PASS = "//label[text()='Admin Portal Password']//parent::*//input[@type='password']"
    NEXT_BUTTON = "//button[text()='Next']"
    BACK_BUTTON = "//button[text()='Back']"
    CANCEL_BUTTON = "//button[text()='Cancel']"

    # PREPARE VM
    PREPARE_VM_BUTTON = "//button[text()='Prepare VM']"
    REDEPLOY_BUTTON = "//button[text()='Redeploy']"
    PREPARE_VM_SUCCESS_TEXT = "//h3[contains(text(), 'successfully')]"

    # STORAGE STAGE
    # NFS
    _STORAGE_TYPE = "//ul[@class='dropdown-menu']/li[@value='%s']"
    STORAGE_BUTTON = _DROPDOWN_MENU % 'Storage Type'
    STORAGE_NFS = _STORAGE_TYPE % 'nfs'
    STORAGE_CONN = _PLACEHOLDER % 'host:/path'
    MNT_OPT = "//label[text()='Mount Options']//parent::*//input[@type='text']"
    STORAGE_ADVANCED = "//form/div[@class='form-group']/child::*//a[text()='Advanced']"
    NFS_VER_DROPDOWN = _DROPDOWN_MENU % 'NFS Version'
    NFS_AUTO = _DROPDOWN_VALUE % 'auto'
    NFS_V3 = _DROPDOWN_VALUE % 'v3'
    NFS_V4 = _DROPDOWN_VALUE % 'v4'
    NFS_V41 = _DROPDOWN_VALUE % 'v4_1'

    # NFS_V42

    # ISCSI
    _TEXT_LABEL = "//label[text()='%s']//parent::*//input[@type='text']"
    _PASSWORD_LABEL = "//label[text()='%s']//parent::*//input[@type='password']"
    STORAGE_ISCSI = _STORAGE_TYPE % 'iscsi'
    PORTAL_IP_ADDR = _TEXT_LABEL % 'Portal IP Address'
    PORTAL_USER = _TEXT_LABEL % 'Portal Username'
    PORTAL_PASS = _PASSWORD_LABEL % 'Portal Password'
    DISCOVERY_USER = _TEXT_LABEL % 'Discovery Username'
    DISCOVERY_PASS = _PASSWORD_LABEL % 'Discovery Password'

    RETRIEVE_TARGET = "//button[text()='Retrieve Target List']"
    SELECTED_TARGET = "//input[@type='radio'][@name='target']"
    SELECTED_ISCSI_LUN = "//input[@type='radio'][@name='lun']"

    # FC
    STORAGE_FC = _STORAGE_TYPE % 'fc'
    SELECTED_FC_LUN = "//input[@type='radio'][@value='36005076300810b3e0000000000000027']"
    FC_DISCOVER = "//button[@text()='Discover']"

    # GLUSTERFS
    STORAGE_GLUSTERFS = _STORAGE_TYPE % 'glusterfs'

    # FINISH STAGE
    FINISH_DEPLOYMENT = "//button[text()='Finish Deployment']"
    CLOSE_BUTTON = "//button[text()='Close']"

    # CHECKPOINTS
    MAINTENANCE_HINT = "//div[contains(text(), 'Local maintenance')]"
    GLOBAL_HINT = "//div[contains(text(), 'global maintenance')]"
    ENGINE_UP_ICON = "//span[contains(@class, 'pficon-ok')]"

    _MAINTENANCE = "//button[contains(text(), '%s')]"
    LOCAL_MAINTENANCE = _MAINTENANCE % 'local'
    REMOVE_MAINTENANCE = _MAINTENANCE % 'Remove'
    GLOBAL_MAINTENANCE = _MAINTENANCE % 'global'

    LOCAL_MAINTEN_STAT = "//div[contains(text(), 'Agent')]"
    VM_STATUS = "//div[contains(text(), 'State')]"
    HE_RUNNING = "//p[contains(text(),'Hosted Engine is running on')]"

    FAILED_TEXT = "//div[text()='Deployment failed']"

    def get_latest_rhvm_appliance(self, appliance_path):
        """
        Purpose:
            Get the latest rhvm appliance from appliance parent path
        """
        req = urllib2.Request(appliance_path)
        rhvm_appliance_html = urllib2.urlopen(req).read()

        mp = MyHTMLParser()
        mp.feed(rhvm_appliance_html)
        mp.close()
        mp.a_texts.sort()

        rhvm42_link_list = []
        all_link = mp.a_texts
        for link in all_link:
            if "4.2" in link:
                rhvm42_link_list.append(link)

        latest_rhvm_appliance_name = rhvm42_link_list[-1]
        latest_rhvm_appliance = appliance_path + latest_rhvm_appliance_name
        return latest_rhvm_appliance

    def install_rhvm_appliance(self, appliance_path):
        rhvm_appliance_link = self.get_latest_rhvm_appliance(appliance_path)
        local_rhvm_appliance = "/root/%s" % rhvm_appliance_link.split('/')[-1]
        self.host.execute("curl -o %s %s" % (local_rhvm_appliance,
                                             rhvm_appliance_link), timeout=200)
        self.host.execute("rpm -ivh %s --force" % local_rhvm_appliance)
        self.host.execute("rm -rf %s" % local_rhvm_appliance)

    def add_to_etc_host(self):
        pass

    def clean_nfs_storage(self, nfs_ip, nfs_pass, nfs_path):
        host_ins = Machine(
            host_string=nfs_ip, host_user='root', host_passwd=nfs_pass)
        host_ins.execute("rm -rf %s/*" % nfs_path)

    def move_failed_setup_log(self):
        cmd = "find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log"
        self.host.execute(cmd)
        if not os.path.exists("/var/old_failed_setup_log"):
            self.host.execute("mkdir -p /var/old_failed_setup_log")
        self.host.execute("mv /var/log/ovirt-hosted-engine-setup/*.log \
                        /var/old_failed_setup_log/")

    def wait_host_up(self, rhvm_ins, host_name, expect_status='up'):
        i = 0
        host_status = "unknown"
        while True:
            if i > 50:
                raise RuntimeError(
                    "Timeout waitting for host %s as current host status is: %s"
                    % (expect_status, host_status))
            host_status = rhvm_ins.list_host("name", host_name)['status']
            if host_status == expect_status:
                break
            elif host_status == 'install_failed':
                raise RuntimeError("Host is not %s as current status is: %s" %
                                   (expect_status, host_status))
            elif host_status == 'non_operational':
                raise RuntimeError("Host is not %s as current status is: %s" %
                                   (expect_status, host_status))
            time.sleep(10)
            i += 1

    def open_page(self):
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.click(self.HOSTEDENGINE_LINK)
        a = self.get_data('ovirt_hostedengine.yml')
        self.config_dict = yaml.load(open(a))

    def prepare_env(self, storage_type='nfs'):
        self.move_failed_setup_log()
        self.install_rhvm_appliance(self.config_dict['rhvm_appliance_path'])
        if storage_type == 'nfs':
            self.clean_nfs_storage(self.config_dict['nfs_ip'],
                                   self.config_dict['nfs_pass'],
                                   self.config_dict['nfs_dir'])
        else:
            pass
            # TODO for iscsi, fc, gluster

    def check_no_password_saved(self, root_pass, admin_pass):
        ret_log = self.host.execute(
            "find /var/log -type f |grep ovirt-hosted-engine-setup-ansible-bootstrap_local_vm.*.log"
        )
        appliance_str = "'APPLIANCE_PASSWORD': '%s'" % root_pass
        appliance_cmd = "grep '%s' %s" % (appliance_str, ret_log)

        admin_str = "'ADMIN_PASSWORD': '%s'" % admin_pass
        admin_cmd = "grep '%s' %s" % (admin_str, ret_log)

        output_appliance_pass = self.host.execute(appliance_cmd)
        output_admin_pass = self.host.execute(admin_cmd)

        if output_appliance_pass or output_admin_pass:
            self.fail()

    def check_no_large_messages(self):
        size1 = self.host.execute(
            "ls -lnt /var/log/messages | awk '{print $5}'")
        time.sleep(10)
        size2 = self.host.execute(
            "ls -lnt /var/log/messages | awk '{print $5}'")
        if int(size2) - int(size1) > 500:
            self.fail()

    def add_additional_host_to_cluster(self, host_ip, host_name, host_pass,
                                       rhvm_fqdn, engine_pass):
        rhvm = RhevmAction(rhvm_fqdn, "admin", engine_pass)
        rhvm.add_host(host_ip, host_name, host_pass, "Default", True)
        self.wait_host_up(rhvm, host_name, 'up')

    def put_host_to_local_maintenance(self):
        self.click(self.LOCAL_MAINTENANCE)
        time.sleep(240)

    def remove_host_from_maintenance(self):
        self.click(self.REMOVE_MAINTENANCE)
        time.sleep(30)

    def put_cluster_to_global_maintenance(self):
        self.click(self.GLOBAL_MAINTENANCE)

    def clean_hostengine_env(self):
        project_path = os.path.dirname(os.path.dirname(__file__))
        clean_he_file = project_path + \
            '/test_suites/test_ovirt_hostedengine.py.data/clean_he_env.py'
        self.host.put_file(clean_he_file, '/root/clean_he_env.py')
        self.host.execute("python /root/clean_he_env.py")

    def check_additional_host_socre(self, ip, passwd):
        cmd = "hosted-engine --vm-status --json"
        host_ins = Machine(
            host_string=ip, host_user='root', host_passwd=passwd)
        i = 0
        while True:
            if i > 10:
                raise RuntimeError(
                    "Timeout waitting for host to available running HE.")
            ret = host_ins.execute(cmd)
            if eval(ret)["2"]["score"] == 3400:
                break
            time.sleep(10)
            i += 1

    def default_vm_engine_stage_config(self):
        # VM STAGE
        self.click(self.HE_START)
        self.input_text(self.VM_FQDN, self.config_dict['he_vm_fqdn'])
        self.input_text(self.MAC_ADDRESS, self.config_dict['he_vm_mac'])
        self.input_text(self.ROOT_PASS, self.config_dict['he_vm_pass'])
        self.click(self.NEXT_BUTTON)

        # ENGINE STAGE
        self.input_text(self.ADMIN_PASS, self.config_dict['admin_pass'])
        self.click(self.NEXT_BUTTON)

        # PREPARE VM
        self.click(self.PREPARE_VM_BUTTON)
        self.click(self.NEXT_BUTTON, 1500)

    def node_zero_default_deploy_process(self):
        def check_deploy():
            self.default_vm_engine_stage_config()

            # STORAGE STAGE
            self.input_text(
                self.STORAGE_CONN,
                self.config_dict['nfs_ip'] + ':' + self.config_dict['nfs_dir'])
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        self.prepare_env('nfs')
        check_deploy()

    def check_no_password_saved_in_setup_log(self):
        self.check_no_password_saved(self.config_dict['he_vm_pass'],
                                     self.config_dict['admin_pass'])

    def node_zero_iscsi_deploy_process(self):
        def check_deploy():
            self.default_vm_engine_stage_config()

            # STORAGE STAGE
            self.click(self.STORAGE_BUTTON)
            self.click(self.STORAGE_ISCSI)
            self.click(self.STORAGE_ADVANCED)
            self.input_text(self.PORTAL_IP_ADDR,
                            self.config_dict['iscsi_portal_ip'])
            self.input_text(self.PORTAL_USER,
                            self.config_dict['iscsi_portal_user'])
            self.input_text(self.PORTAL_PASS,
                            self.config_dict['iscsi_portal_pass'])
            self.input_text(self.DISCOVERY_USER,
                            self.config_dict['iscsi_discovery_user'])
            self.input_text(self.DISCOVERY_PASS,
                            self.config_dict['iscsi_discovery_pass'])

            self.click(self.RETRIEVE_TARGET)
            self.click(self.SELECTED_TARGET, 60)
            self.click(self.SELECTED_ISCSI_LUN, 60)
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        self.prepare_env('iscsi')
        check_deploy()

    def node_zero_fc_deploy_process(self):
        def check_deploy():
            self.default_vm_engine_stage_config()

            # STORAGE STAGE
            self.click(self.STORAGE_BUTTON)
            self.click(self.STORAGE_FC)

            self.click(self.SELECTED_FC_LUN, 60)

            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        self.prepare_env('fc')
        check_deploy()

    def node_zero_gluster_deploy_process(self):
        def check_deploy():
            self.default_vm_engine_stage_config()

            # STORAGE STAGE
            self.click(self.STORAGE_BUTTON)
            self.click(self.STORAGE_GLUSTERFS)
            self.input_text(
                self.STORAGE_CONN,
                self.config_dict['gluster_ip'] + ':' + self.config_dict['gluster_dir'])
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        self.prepare_env('gluster')
        check_deploy()

    def node_zero_static_v4_deploy_process(self):
        def check_deploy():
            # VM STAGE
            self.click(self.HE_START)
            self.input_text(self.VM_FQDN, self.config_dict['he_vm_fqdn'])
            self.input_text(self.MAC_ADDRESS, self.config_dict['he_vm_mac'])
            self.click(self.NETWORK_DROPDOWN)
            self.click(self.NETWORK_STATIC)
            self.input_text(self.VM_IP, self.config_dict['he_vm_ip'])
            self.input_text(self.IP_PREFIX, self.config_dict['he_ip_prefix'])
            self.input_text(self.DNS_SERVER, self.config_dict['dns_server'])
            self.input_text(self.ROOT_PASS, self.config_dict['he_vm_pass'])
            self.click(self.NEXT_BUTTON)

            # ENGINE STAGE
            self.input_text(self.ADMIN_PASS, self.config_dict['admin_pass'])
            self.click(self.NEXT_BUTTON)

            # PREPARE VM
            self.click(self.PREPARE_VM_BUTTON)
            self.click(self.NEXT_BUTTON, 1500)

            # STORAGE STAGE
            self.input_text(
                self.STORAGE_CONN,
                self.config_dict['nfs_ip'] + ':' + self.config_dict['nfs_dir'])
            self.click(self.STORAGE_ADVANCED)
            self.click(self.NFS_VER_DROPDOWN)
            self.click(self.NFS_V4)
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        self.prepare_env('nfs')
        check_deploy()

    def hostedengine_redeploy_process(self):
        self.clean_hostengine_env()
        self.refresh()
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.node_zero_default_deploy_process()

    def add_additional_host_to_cluster_process(self):
        self.add_additional_host_to_cluster(
            self.config_dict['second_host'], self.config_dict['second_vm_fqdn'],
            self.config_dict['second_pass'], self.config_dict['he_vm_fqdn'],
            self.config_dict['admin_pass'])
        self.check_additional_host_socre(self.config_dict['second_host'],
                                         self.config_dict['second_pass'])

    def check_local_maintenance(self):
        self.put_host_to_local_maintenance()

    def check_remove_maintenance(self):
        self.remove_host_from_maintenance()

    def check_global_maintenance(self):
        self.put_cluster_to_global_maintenance()
