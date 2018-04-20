import os
import time
import simplejson
import urllib2
from page import PageTest
from utils.htmlparser import MyHTMLParser
from utils.machine import Machine
from utils.rhvmapi import RhevmAction


class OvirtHostedEnginePage(PageTest):
    """
    :avocado: disable
    """

    OVIRT_HOSTEDENGINE_FRAME_NAME = "/ovirt-dashboard"
    HOSTEDENGINE_LINK = "XPATH{}//a[@href='#/he']"

    # Start button
    HE_START = "XPATH{}//span[@class='deployment-option-panel-container']/button[text()='Start']"

    # Guide Links
    GETTING_START_LINK = "XPATH{}//a[contains(@href, 'Self-Hosted_Engine_Guide')]"
    MORE_INFORMATION_LINK = "XPATH{}//a[contains(@href, 'www.ovirt.org')]"

    # VM STAGE
    _TITLE = "XPATH{}//input[@title='%s']"
    _PLACEHOLDER = "XPATH{}//input[@placeholder='%s']"
    VM_FQDN = _PLACEHOLDER % 'ovirt-engine.example.com'
    MAC_ADDRESS = _TITLE % 'Enter the MAC address for the VM.'
    ROOT_PASS = "XPATH{}//label[text()='Root Password']//parent::*//input[@type='password']"
    ADVANCED = "XPATH{}//a[text()='Advanced']"

    # TODO
    _DROPDOWN_MENU = "XPATH{}//label[text()='%s]//parent::*//button[contains(@class, 'dropdown-toggle')]"
    NETWORK_DROPDOWN = _DROPDOWN_MENU % 'Network Configuration'
    # TODO
    # BRIDGE_DROPDOWN
    SSH_ACCESS_DROPDOWN = _DROPDOWN_MENU % 'Root SSH Access'
    _DROPDOWN_VALUE = "XPATH{}//ul[@class='dropdown-menu']/li[@value='%s']"
    NETWORK_DHCP = _DROPDOWN_VALUE % 'dhcp'

    NETWORK_STATIC = _DROPDOWN_VALUE % 'static'
    VM_IP = _PLACEHOLDER % '192.168.1.2'
    DNS_SERVER = "XPATH{}//div[contains(@class, 'multi-row-text-box-input')]" \
        "/input[@type='text']"

    # ENGINE STAGE
    ADMIN_PASS = "XPATH{}//label[text()='Admin Portal Password']//parent::*//input[@type='password']"
    NEXT_BUTTON = "XPATH{}//button[text()='Next']"
    BACK_BUTTON = "XPATH{}//button[text()='Back']"
    CANCEL_BUTTON = "XPATH{}//button[text()='Cancel']"

    # PREPARE VM
    PREPARE_VM_BUTTON = "XPATH{}//button[text()='Prepare VM']"
    REDEPLOY_BUTTON = "XPATH{}//button[text()='Redeploy']"
    PREPARE_VM_SUCCESS_TEXT = "XPATH{}//h3[contains(text(), 'successfully')]"

    # STORAGE STAGE
    # NFS
    _STORAGE_TYPE = "XPATH{}//ul[@class='dropdown-menu']/li[@value='%s']"
    STORAGE_NFS = _STORAGE_TYPE % 'nfs'
    STORAGE_CONN = _PLACEHOLDER % 'host:/path'
    MNT_OPT = "XPATH{}//label[text()='Mount Options']//parent::*//input[@type='text']"
    NFS_VER_DROPDOWN = _DROPDOWN_MENU % 'NFS Version'
    NFS_AUTO = _DROPDOWN_VALUE % 'auto'
    NFS_V3 = _DROPDOWN_VALUE % 'v3'
    NFS_V4 = _DROPDOWN_VALUE % 'v4'
    NFS_V41 = _DROPDOWN_VALUE % 'v4_1'
    # NFS_V42

    # ISCSI
    STORAGE_ISCSI = _STORAGE_TYPE % 'iscsi'
    PORTAL_IP_ADDR = _TITLE % 'Enter the IP address for the iSCSI portal you wish to use.'
    PORTAL_USER = "XPATH{}//input[@title='Enter the user for the iSCSI portal you wish to use.'][@type='text']"
    PORTAL_PASS = "XPATH{}//input[@title='Enter the user for the iSCSI portal you wish to use.'][@type='password']"
    # DISCOVERY_USER
    # DISCOVERY_PASS
    RETRIEVE_TARGET = "XPATH{}//button[text()='Retrieve Target List']"
    # SELECTED_TARGET
    # SELECTED_ISCSI_LUN

    # FC
    STORAGE_FC = _STORAGE_TYPE % 'fc'
    # SELECTED_FC_LUN
    # FC_DISCOVER = "XPATH{}//button[@class='btn btn-primary']"

    # GLUSTERFS
    STORAGE_GLUSTERFS = _STORAGE_TYPE % 'glusterfs'

    # FINISH STAGE
    FINISH_DEVELOPMENT = "XPATH{}//button[text()='Finish Development']"
    CLOSE_BUTTON = "XPATH{}//button[text()='Close']"

    # CHECKPOINTS
    MAINTENANCE_HINT = "XPATH{}//div[text()='Local maintenance cannot be enabled with a single host']"
    GLOBAL_HINT = "XPATH{}//div[text()='The cluster is in global maintenance mode!']"
    ENGINE_UP_ICON = "XPATH{}//span[contains(@class, 'pficon-ok')]"

    _MAINTENANCE = "XPATH{}//button[contains(text(), '%s')]"
    LOCAL_MAINTENANCE = _MAINTENANCE % 'local'
    REMOVE_MAINTENANCE = _MAINTENANCE % 'Remove'
    GLOBAL_MAINTENANCE = _MAINTENANCE % 'global'

    LOCAL_MAINTEN_STAT = "XPATH{}//div[@class='list-group-item-text']"
    VM_STATUS = "XPATH{}//div[contains(@class, 'list-view-pf-additional-info-item')]/div"
    HE_RUNNING = "XPATH{}//p[contains(text(),'Hosted Engine is running on')]"
    
    FAILED_TEXT = "XPATH{}//div[text()='Deployment failed']"

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
        output = self.host.execute(
            "curl -o %s %s" % (local_rhvm_appliance, rhvm_appliance_link))
        if output[0] == "False":
            raise Exception(
                "ERR: Failed to download the latest rhvm appliance")

        self.host.execute("rpm -ivh %s --force" % local_rhvm_appliance)
        self.host.execute("rm -rf %s" % local_rhvm_appliance)

    def add_to_etc_host(self):
        pass

    def clean_nfs_storage(self, nfs_ip, nfs_pass, nfs_path):
        host_ins = Machine(host_string=nfs_ip, host_user='root', host_passwd=nfs_pass)
        host_ins.execute("rm -rf %s/*" % nfs_path)

    def move_failed_setup_log(self):
        cmd = "find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log"
        ret = self.host.execute(cmd)
        if ret[0] == True:
            if os.path.exists("/var/old_failed_setup_log") == False:
                self.host.execute("mkdir -p /var/old_failed_setup_log")
            self.host.execute("mv /var/log/ovirt-hosted-engine-setup/*.log \
                         /var/old_failed_setup_log/")
        else:
            pass

    def wait_host_status(self, rhvm_ins, host_name, expect_status):
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
        self.browser.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.browser.click(self.HOSTEDENGINE_LINK)

    def check_no_password_saved(self, root_pass, admin_pass):
        ret_log = self.host.execute(
            "find /var/log -type f |grep ovirt-hosted-engine-setup-bootstrap_local_vm.*.log")
        appliance_cmd = "grep 'APPLIANCE_PASSWORD': '%s' %s" % (
            root_pass, ret_log[1])
        admin_cmd = "grep 'ADMIN_PASSWORD': '%s' %s" % (admin_pass, ret_log[1])
        output_appliance_pass = self.host.execute(appliance_cmd)
        output_admin_pass = self.host.execute(admin_cmd)

        if output_appliance_pass or output_admin_pass:
            raise Exception(
                "ERR: The appliance and admin passwords are saved.")

    def check_no_large_messages(self):
        size1 = self.host.execute(
            "ls -lnt /var/log/messages | awk '{print $5}'")
        time.sleep(10)
        size2 = self.host.execute(
            "ls -lnt /var/log/messages | awk '{print $5}'")
        if int(size2[1]) - int(size1[1]) > 200:
            raise Exception(
                "Look like large messages under /var/log/messages, please check")

    def add_additional_host_to_cluster(self, host_ip, host_name, host_pass, rhvm_fqdn, engine_pass):
        rhvm = RhevmAction(rhvm_fqdn, "admin", engine_pass)
        rhvm.add_host(host_ip, host_name, host_pass, "Default", True)
        if not self.wait_host_status(rhvm, host_name, 'up'):
            raise Exception(
                "ERR: Add the additional host to the cluster failed, pls check.")

    def put_host_to_local_maintenance(self):
        self.browser.click(self.LOCAL_MAINTENANCE)
        time.sleep(120)

    def remove_host_from_maintenance(self):
        self.browser.click(self.REMOVE_MAINTENANCE)
        time.sleep(30)

    def put_cluster_to_global_maintenance(self):
        self.browser.click(self.GLOBAL_MAINTENANCE)

    def clean_hostengine_env(self):
        project_path = os.path.dirname(os.path.dirname(__file__))
        clean_rnv_file = ''.join(project_path) + '/utils/clean_he_env.py'
        self.host.put_file(clean_rnv_file, '/root/clean_he_env.py')
        self.host.execute("python /root/clean_he_env.py")


