import os
import yaml
import time
import datetime
import simplejson
import urllib2
import stat
from seleniumlib import SeleniumTest
from utils.htmlparser import MyHTMLParser
from utils.machine import Machine
from utils.rhvmapi import RhevmAction


class OvirtHostedEnginePage(SeleniumTest):
    """
    :avocado: disable
    """

    # GENERAL
    OVIRT_HOSTEDENGINE_FRAME_NAME = "/ovirt-dashboard"
    HOSTEDENGINE_LINK = "//a[@href='#/he']"

    # LANDING PAGE
    ## Start button
    HE_START = "//span[@class='deployment-option-panel-container']/button[@id='he-wizard-btn']"

    ## Guide Links
    GETTING_START_LINK = "//a[contains(text(), 'Installation Guide')]"
    MORE_INFORMATION_LINK = "//a[contains(text(), 'RHV Documentation')]"

    # VM STAGE
    VM_PAGE_ERR = "//div[@id='he-errors-on-page-err']/div/strong[text()='Please correct errors before moving to the next step.']"
    VM_FQDN_INVALID_ERR = "//span[@id='he-invalid-engine-fqdn-err']"
    HOST_FQDN_INVALID_ERR = "//span[@id='he-invalid-host-fqdn-err']"
    GATEWAY_INVALID_ERR = "//span[@id='he-static-ip-invalid-gateway']"
    # VM_MEM_WARN = "//div[@id='he-not-enough-memory-warn']/strong[text()='xxxxxxxxxxx']"   #No environment.
    VM_FQDN_VALIDATING_WARN = "//div[@id='he-validating-fqdn-warn']/div/strong[text()='FQDN validation is in progress. Please wait for validation to complete and try again.']"
    VM_FQDN_INVALID_WARN = "//div[@id='he-invalid-engine-fqdn-warn']/div/strong[text()='The VM FQDN could not be resolved. Please ensure that the FQDN is resolvable before attempting preparation of the VM.']"
    HOST_FQDN_INVALID_WARN = "//div[@id='he-invalid-host-fqdn-warn']"
    
    VM_FQDN = "//label[text()='Engine VM FQDN']//parent::*//input[@id='he-engine-fqdn-input']"
    VM_FQDN_VALIDATING_MSG = "//label[text()='Engine VM FQDN']//parent::*//span//span[@id='he-validating-engine-fqdn-msg']"
    MAC_ADDRESS = "//input[@id='he-engine-mac-address-input']"
    ROOT_PASS = "//label[text()='Root Password']//parent::*//input[@type='password']"
    
    VM_ADVANCED = "//a[@id='he-advanced-menu']"
    # VM_SSH_PUB_KEY_TETAREA = "//textarea[@id='he-ssh-pubkey-input']"
    # VM_ETC_HOSTS_CHKBOX = "//input[@id='he-edit-etc-hosts-chkbox']"
    # VM_BRIDGE_NAME_INPUT = "//input[@id='he-bridge-name-input']"
    VM_DEFAULT_GATEWAY_INPUT = "//input[@id='he-default-gateway-input']"
    DEFAULT_GATEWAY_INVALID_ERR = "//span[@id='he-invalid-default-gateway-err']"
    # VM_VCPU_NUM_INPUT = "//input[@id='he-vcpus-number-input']"
    # VM_MEM_SIZE_INPUT = "//input[@id='he-memory-size-input']"
    HOST_FQDN_INPUT = "//input[@id='he-host-fqdn-input']"
    HOST_FQDN_VALIDATING_MSG = "//span[@id='he-validating-host-fqdn-msg']"

    ## VM NETWORK
    _DROPDOWN_MENU = "//label[text()='%s']//parent::*//button[contains(@class, 'dropdown-toggle')]"
    NETWORK_DROPDOWN = _DROPDOWN_MENU % 'Network Configuration'

    ### BRIDGE_DROPDOWN
    SSH_ACCESS_DROPDOWN = _DROPDOWN_MENU % 'Root SSH Access'
    _DROPDOWN_VALUE = "//ul[@class='dropdown-menu']/li[@value='%s']"
    NETWORK_DHCP = _DROPDOWN_VALUE % 'dhcp'

    NETWORK_STATIC = _DROPDOWN_VALUE % 'static'
    VM_IP = "//input[@id='he-static-ip-address-input']"
    IP_PREFIX = "//input[@placeholder='%s']" % '24'
    GATEWAY_INPUT = "//input[@id='he-static-ip-gateway-input']"
    DNS_SERVER = "//div[contains(@class, 'multi-row-text-box-input')]" \
        "/input[@type='text']"

    # ENGINE STAGE
    ENGINE_PAGE_ERR = "//span[@id='he-errors-on-page-err']//parent::*//strong[text()='Please correct errors before moving to the next step.']"
    ADMIN_PASS_ERR = "//span[@id='he-admin-password-err']"
    ADMIN_PASS = "//input[@id='he-admin-password-input']"
    # NOTIFICATION_SERVER_INPUT = "//input[@id='he-notification-server-input']"
    # NOTIFICATION_SERVER_PORT_INPUT = "//input[@id='he-notification-smtp-port-input']"
    # SENDER_EMAIL_ADDR_INPUT = "//input[@id='he-sender-email-input']"
    NEXT_BUTTON = "//button[text()='Next']"
    BACK_BUTTON = "//button[text()='Back']"
    CANCEL_BUTTON = "//button[text()='Cancel']"

    # PREPARE VM
    PREPARE_VM_BUTTON = "//button[text()='Prepare VM']"
    REDEPLOY_BUTTON = "//button[text()='Redeploy']"
    PREPARE_VM_SUCCESS_TEXT = "//h3[contains(text(), 'successfully')]"

    # STORAGE STAGE
    ## NFS
    _STORAGE_TYPE = "//ul[@class='dropdown-menu']/li[@value='%s']"
    STORAGE_BUTTON = _DROPDOWN_MENU % 'Storage Type'
    STORAGE_NFS = _STORAGE_TYPE % 'nfs'
    STORAGE_CONN = "//input[@placeholder='%s']" % 'host:/path'
    MNT_OPT = "//label[text()='Mount Options']//parent::*//input[@type='text']"
    STORAGE_ADVANCED = "//form/div[@class='form-group']/child::*//a[text()='Advanced']"
    NFS_VER_DROPDOWN = _DROPDOWN_MENU % 'NFS Version'
    NFS_AUTO = _DROPDOWN_VALUE % 'auto'
    NFS_V3 = _DROPDOWN_VALUE % 'v3'
    NFS_V4 = _DROPDOWN_VALUE % 'v4'
    NFS_V41 = _DROPDOWN_VALUE % 'v4_1'

    ## ISCSI
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

    ## FC
    STORAGE_FC = _STORAGE_TYPE % 'fc'
    SELECTED_FC_LUN = "//input[@type='radio'][@value='36005076300810b3e0000000000000027']"
    FC_DISCOVER = "//button[@text()='Discover']"

    ## GLUSTERFS
    STORAGE_GLUSTERFS = _STORAGE_TYPE % 'glusterfs'

    # FINISH STAGE
    FINISH_DEPLOYMENT = "//button[text()='Finish Deployment']"
    CLOSE_BUTTON = "//button[text()='Close']"

    # DEPLOYED PAGE
    ## HINT&ICON
    MIGRATION_HINT = "//div[contains(text(), 'please migrate it')]"
    MAINTENANCE_HINT = "//div[contains(text(), 'Local maintenance')]"
    GLOBAL_HINT = "//div[contains(text(), 'global maintenance')]"
    ENGINE_UP_ICON = "//span[contains(@class, 'pficon-ok')]"
    ## MAINTENANCE BUTTONS
    _MAINTENANCE = "//button[contains(text(), '%s')]"
    LOCAL_MAINTENANCE = _MAINTENANCE % 'local'
    REMOVE_MAINTENANCE = _MAINTENANCE % 'Remove'
    GLOBAL_MAINTENANCE = _MAINTENANCE % 'global'
    ## STATUS
    LOCAL_MAINTEN_STAT = "//div[contains(text(), 'Agent')]"
    VM_STATUS = "//div[contains(text(), 'State')]"
    HE_RUNNING = "//p[contains(text(),'Hosted Engine is running on')]"
    FAILED_TEXT = "//div[text()='Deployment failed']"
    RECONNECT_BUTTON = "//button[text()='Reconnect']"

    # override functions
    def setUp(self):
        case_name = self._testMethodName
        config = self.get_data('ovirt_hostedengine.yml')
        self.config_dict = yaml.load(open(config))
       
        if 'fc' in case_name.split('_'):
            os.environ['HOST_STRING'] = self.config_dict['host_fc_string']
        if 'port' in case_name.split('_'):
            os.environ['HOST_PORT'] = '9898'
        super(OvirtHostedEnginePage,self).setUp()

    def open_page(self):
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.click(self.HOSTEDENGINE_LINK)
    
    # internal functions
    def backup_remove_logs(self):
        log_backup = os.path.join('/var/old_hosted_engine_log/',datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        self.host.execute("mkdir -p {}".format(log_backup))

        for filter in ['ovirt-hosted-engine-setup*','agent','broker','HostedEngine*']:
            cmd = "find /var/log -type f |grep {}".format(filter)
            try:
                log_list = self.host.execute(cmd).rsplit("\n")
                for each_entry in log_list:
                    self.host.execute("mv {0} {1}".format(each_entry.replace("\r",""),log_backup))
            except Exception as e:
                pass
            finally:
                self.host.execute("rm -rf /var/log/ovirt-hosted-engine-setup/*",raise_exception=False)

    def get_rhvm_appliance(self, appliance_path):
        req = urllib2.Request(appliance_path)
        rhvm_appliance_html = urllib2.urlopen(req).read()

        mp = MyHTMLParser()
        mp.feed(rhvm_appliance_html)
        mp.close()
        mp.a_texts.sort()

        rhvm_appliance_dict = {'v4.2':[], 'v4.3':[], 'v4.4':[]}
        all_appliance = mp.a_texts
        for appliance in all_appliance:
            if "-4.2-" in appliance:
                rhvm_appliance_dict.get('v4.2').append(appliance)
            elif "-4.3-" in appliance:
                rhvm_appliance_dict.get('v4.3').append(appliance)
            elif "-4.4-" in appliance:
                rhvm_appliance_dict.get('v4.4').append(appliance)
        
        img_ver = self.host.execute("imgbase w", raise_exception=False).split(' ')[-1]
        if '4.2' in img_ver:
            rhvm_appliance = rhvm_appliance_dict.get('v4.2')[-1]
        elif '4.3' in img_ver:
            rhvm_appliance = rhvm_appliance_dict.get('v4.3')[-1]
        elif '4.4' in img_ver:
            rhvm_appliance = rhvm_appliance_dict.get('v4.4')[-1]
        rhvm_appliance_link = appliance_path + rhvm_appliance
        return rhvm_appliance_link

    def install_rhvm_appliance(self, appliance_path):
        rhvm_appliance_link = self.get_rhvm_appliance(appliance_path)
        try:
            # for STIG, need to add option "--nogpgcheck"
            self.host.execute("yum install -y {}".format(rhvm_appliance_link))
        except Exception as e:
            pass

    def prepare_env(self, storage_type='nfs'):
        additional_host = Machine(host_string=self.config_dict['second_host'], host_user='root', host_passwd=self.config_dict['second_pass'])
        if additional_host.execute('hosted-engine --check-deployed',raise_exception=False).stdout == "":
            additional_host.execute("yes|sh /usr/sbin/ovirt-hosted-engine-cleanup", timeout=250)

        if self.host.execute('rpm -qa|grep appliance',raise_exception=False).stdout == "":
            self.install_rhvm_appliance(self.config_dict['rhvm_appliance_path'])

        if self.host.execute('hosted-engine --check-deployed', raise_exception=False).stdout == "":
            self.backup_remove_logs()
            self.clean_hostengine_env()
            self.refresh()
            self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)

        if storage_type == 'nfs':
            self.clean_nfs_storage(self.config_dict['nfs_ip'],
                                   self.config_dict['nfs_pass'],
                                   self.config_dict['nfs_dir'])
        elif storage_type == 'iscsi':
            try:
                self.host.get_file('/etc/iscsi/initiatorname.iscsi','./initiatorname.iscsi')
                new_line = ''
                with open('./initiatorname.iscsi') as config_file:
                    for line in config_file:
                        if line.startswith('InitiatorName'):
                            new_line = line.replace(line.split('=')[-1],self.config_dict['iscsi_initiator_name'])
                with open('./initiatorname.iscsi', 'w') as config_file:
                    config_file.write(new_line)
                self.host.put_file('./initiatorname.iscsi','/etc/iscsi/initiatorname.iscsi')
                os.remove('./initiatorname.iscsi')
                self.host.execute('systemctl restart iscsid iscsi')
                self.clean_iscsi_storage(self.config_dict['iscsi_portal_ip'])
            except Exception as e:
                pass           
        elif storage_type == 'fc':
            luns_fc_storage = self.config_dict['luns_fc_storage']
            for lun_id in luns_fc_storage:
                # self.clean_fc_storage(lun_id)
                pass      
        elif storage_type == 'gluster':
            glusterfs_servers = list(self.config_dict['gluster_ips'].values())
            for ip in glusterfs_servers:
                self.clean_glusterfs_storage_pre(ip, self.config_dict['root_passwd'])
            self.clean_glusterfs_storage_post(glusterfs_servers[0],self.config_dict['root_passwd'])
    
    def clean_nfs_storage(self, nfs_ip, nfs_pass, nfs_path):
        try:
            host_ins = Machine(
                host_string=nfs_ip, host_user='root', host_passwd=nfs_pass)
            host_ins.execute("rm -rf %s/*" % nfs_path)
        except:
            import traceback
            traceback.print_exc()
            self.fail()

    def clean_fc_storage(self, id):
        cmd = 'dd if=/dev/zero of=/dev/mapper/{} bs=10M'.format(id)
        try:
            self.host.execute(cmd,timeout=2000,raise_exception=False)
        except:
            import traceback
            traceback.print_exc()
            self.fail()

    def clean_iscsi_storage(self, iscsi_ip):
        try:
            str = self.host.execute('iscsiadm --mode discoverydb --type sendtargets --portal {} --discover'.format(iscsi_ip))
            print(str.split(' ')[-1])
            self.host.execute('iscsiadm --mode node --targetname {0} --portal {1}:3260 --login'.format(str.split(' ')[-1], iscsi_ip))
            self.host.execute('dd if=/dev/zero of=/dev/sdb bs=10M', timeout=2000,raise_exception=False)
            self.host.execute('iscsiadm --mode node --targetname {0} --portal {1}:3260 --logout'.format(str.split(' ')[-1], iscsi_ip))
        except:
            import traceback
            traceback.print_exc()
            self.fail()

    def clean_glusterfs_storage_pre(self, glusterfs_ip, password):
        host_glusterfs_server = Machine(host_string=glusterfs_ip, host_user='root', host_passwd=password)
        try:
            if glusterfs_ip == list(self.config_dict['gluster_ips'].values())[0]:
                host_glusterfs_server.execute("yes|gluster volume stop {}".format(self.config_dict['gluster_volume']), raise_exception=False)
                host_glusterfs_server.execute("yes|gluster v delete {}".format(self.config_dict['gluster_volume']), raise_exception=False)
            host_glusterfs_server.execute("umount {}".format(self.config_dict['gluster_volume_mount']))
            host_glusterfs_server.execute("mkfs.ext4 /dev/sdb1")
            host_glusterfs_server.execute("mount /dev/sdb1 {}".format(self.config_dict['gluster_volume_mount']))
            host_glusterfs_server.execute("mkdir {0}/{1}".format(self.config_dict['gluster_volume_mount'],self.config_dict['gluster_volume']))
        except:
            import traceback
            traceback.print_exc()
            self.fail()

    def clean_glusterfs_storage_post(self, glusterfs_ip, password):
        host_glusterfs_server = Machine(host_string=glusterfs_ip, host_user='root', host_passwd=password)
        try:
            #host_glusterfs_server.execute("gluster v create gv1 replica 3 bootp-73-131-238.rhts.eng.pek2.redhat.com:/data/gluster/gv1 bootp-73-131-184.rhts.eng.pek2.redhat.com:/data/gluster/gv1 bootp-73-131-188.rhts.eng.pek2.redhat.com:/data/gluster/gv1")  
            host_glusterfs_server.execute("gluster v create gv1 replica 3 {0}:/data/gluster/gv1 {1}:/data/gluster/gv1 {2}:/data/gluster/gv1".format(*self.config_dict['gluster_ips'].keys()))
            host_glusterfs_server.execute("gluster volume set gv1 cluster.quorum-type auto")
            host_glusterfs_server.execute("gluster volume set gv1 network.ping-timeout 10")
            host_glusterfs_server.execute("gluster volume set gv1 auth.allow \*")
            host_glusterfs_server.execute("gluster volume set gv1 group virt")
            host_glusterfs_server.execute("gluster volume set gv1 storage.owner-uid 36")
            host_glusterfs_server.execute("gluster volume set gv1 storage.owner-gid 36")
            host_glusterfs_server.execute("gluster volume set gv1 server.allow-insecure on")
            host_glusterfs_server.execute("gluster volume start {}".format(self.config_dict['gluster_volume']))
        except:
            import traceback
            traceback.print_exc()
            self.fail()

    def default_vm_engine_stage_config(self):
        # VM STAGE
        self.click(self.HE_START)
        time.sleep(100)
        self.input_text(self.VM_FQDN, self.config_dict['he_vm_fqdn'], 60)
        self.input_text(self.MAC_ADDRESS, self.config_dict['he_vm_mac'])
        self.input_text(self.ROOT_PASS, self.config_dict['he_vm_pass'])
        self.assert_text_in_element(self.VM_FQDN_VALIDATING_MSG, "Validating FQDN...")
        time.sleep(120)
        self.click(self.NEXT_BUTTON)

        # ENGINE STAGE
        self.input_text(self.ADMIN_PASS, self.config_dict['admin_pass'])
        self.click(self.NEXT_BUTTON)

        # PREPARE VM
        self.click(self.PREPARE_VM_BUTTON)
        self.click(self.NEXT_BUTTON, 2200)

    def check_no_password_saved(self, root_pass, admin_pass):
        ret_log = self.host.execute(
            "find /var/log -type f |grep ovirt-hosted-engine-setup-ansible-bootstrap_local_vm.*.log"
        )
        appliance_str = "'APPLIANCE_PASSWORD': u'%s'" % root_pass
        appliance_cmd = 'grep "%s" %s' % (appliance_str, ret_log)

        admin_str = "'ADMIN_PASSWORD': u'%s'" % admin_pass
        admin_cmd = 'grep "%s" %s' % (admin_str, ret_log)

        output_appliance_pass = self.host.execute(appliance_cmd, raise_exception=False)
        output_admin_pass = self.host.execute(admin_cmd, raise_exception=False)

        if output_admin_pass.succeeded or output_appliance_pass.succeeded:
            self.fail()

    def add_additional_host_to_cluster(self, host_ip, host_name, host_pass,
                                       rhvm_fqdn, engine_pass):
        rhvm = RhevmAction(rhvm_fqdn, "admin", engine_pass)
        rhvm.add_host(host_ip, host_name, host_pass, "Default", True)
        self.wait_host_up(rhvm, host_name, 'up')

    def add_normal_host_to_cluster(self, host_ip, host_name, host_pass,
                                       rhvm_fqdn, engine_pass):
        rhvm = RhevmAction(rhvm_fqdn, "admin", engine_pass)
        rhvm.add_host(host_ip, host_name, host_pass, "Default")
        self.wait_host_up(rhvm, host_name, 'up')

    def migrate_vms(self, vm_name, dest_host_fqdn, rhvm_fqdn, engine_pass):
        rhvm = RhevmAction(rhvm_fqdn, 'admin', engine_pass)
        rhvm.migrate_vm(vm_name, dest_host_fqdn)
        # self.wait_migrated(rhvm, vm_name)

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
            time.sleep(15)
            i += 1

    def wait_migrated(self, rhvm_ins, vm_name, expect_status='up'):
        i = 0
        vm_status = "unknown"
        while True:
            if i > 50:
                raise RuntimeError(
                    "Timeout waitting for vm migration %s as current vm status is: %s"
                    %(expect_status, vm_status)
                )
            time.sleep(20)
            vm_status = rhvm_ins.list_vm(vm_name)['status']
            if vm_status == 'migrating':
                i = i + 1
            elif vm_status == 'up':
                break

    def check_additional_host_socre(self, ip, passwd):
        true, false = True, False
        cmd = "hosted-engine --vm-status --json"
        host_ins = Machine(
            host_string=ip, host_user='root', host_passwd=passwd)
        i = 0
        while True:
            if i > 10:
                raise RuntimeError(
                    "Timeout waitting for host to available running HE.")
            print(cmd)
            ret = host_ins.execute(cmd)
            if eval(ret)["2"]["score"] == 3400:
                break
            time.sleep(15)
            i += 1
    
    def put_host_to_local_maintenance(self):
        self.click(self.LOCAL_MAINTENANCE)
        time.sleep(30)

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
        self.host.execute("python /root/clean_he_env.py", timeout=160)

    def setting_to_non_default_port(self):
        project_path = os.path.dirname(os.path.dirname(__file__))
        non_default_port_file = project_path + \
            '/test_suites/test_ovirt_hostedengine.py.data/non_default_port.py'
        self.host.put_file(non_default_port_file, '/root/non_default_port.py')
        self.host.execute("python /root/non_default_port.py", timeout=60)

    def setting_to_default_port(self):
        project_path = os.path.dirname(os.path.dirname(__file__))
        default_port_file = project_path + \
            '/test_suites/test_ovirt_hostedengine.py.data/default_port.py'
        self.host.put_file(default_port_file, '/root/default_port.py')
        self.host.execute("python /root/default_port.py", timeout=60)

    ## Cases
    # tier1_0
    def errors_warnings_vm_setting(self):           
        self.click(self.HE_START)
        time.sleep(40)
        self.click(self.NEXT_BUTTON)
        self.assert_element_visible(self.VM_PAGE_ERR)
        self.assert_text_in_element(self.VM_PAGE_ERR, "Please correct errors before moving to the next step.")
        self.assert_element_visible(self.VM_FQDN_INVALID_ERR)
        self.assert_text_in_element(self.VM_FQDN_INVALID_ERR, "Required field")

        self.input_text(self.VM_FQDN, "invalid", 60)
        self.input_text(self.ROOT_PASS, self.config_dict['he_vm_pass'])
        self.click(self.NEXT_BUTTON)
        self.assert_text_in_element(self.VM_FQDN_VALIDATING_WARN, "FQDN validation is in progress. Please wait for validation to complete and try again.")
        time.sleep(40)
        self.assert_element_visible(self.VM_FQDN_INVALID_WARN)
        self.assert_text_in_element(self.VM_FQDN_INVALID_WARN, "The VM FQDN could not be resolved. Please ensure that the FQDN is resolvable before attempting preparation of the VM.")
        self.assert_element_visible(self.VM_FQDN_INVALID_ERR)
        self.assert_text_in_element(self.VM_FQDN_INVALID_ERR, "Unable to resolve address")

        self.click(self.VM_ADVANCED)
        self.input_text(self.HOST_FQDN_INPUT, "invalid", 60)
        self.click(self.NEXT_BUTTON)
        self.assert_text_in_element(self.HOST_FQDN_VALIDATING_MSG, "Validating FQDN...")
        time.sleep(40)
        self.assert_text_in_element(self.HOST_FQDN_INVALID_ERR, "Unable to resolve address")
        # self.assert_element_visible(self.HOST_FQDN_INVALID_WARN)
        self.input_text(self.VM_DEFAULT_GATEWAY_INPUT, "10.73", 60)
        self.assert_text_in_element(self.DEFAULT_GATEWAY_INVALID_ERR, "Invalid format for IP address")


        self.click(self.NETWORK_DROPDOWN)
        self.click(self.NETWORK_STATIC)
        self.input_text(self.GATEWAY_INPUT, "10.73.254", 60)
        time.sleep(5)
        self.assert_element_visible(self.GATEWAY_INVALID_ERR)
        self.assert_text_in_element(self.GATEWAY_INVALID_ERR, "Invalid format for IP address")

    def errors_warnings_engine_setting(self):
        self.click(self.HE_START)
        time.sleep(60)
        self.input_text(self.VM_FQDN, self.config_dict['he_vm_fqdn'], 60)
        self.input_text(self.MAC_ADDRESS, self.config_dict['he_vm_mac'])
        self.input_text(self.ROOT_PASS, self.config_dict['he_vm_pass'])
        time.sleep(60)
        self.click(self.NEXT_BUTTON)
        time.sleep(5)
        self.click(self.NEXT_BUTTON)
        self.assert_text_in_element(self.ENGINE_PAGE_ERR, "Please correct errors before moving to the next step.")
        self.assert_text_in_element(self.ADMIN_PASS_ERR, "Required field")

    # tier1_1
    def node_zero_default_deploy_process(self):
        def check_deploy():
            self.refresh()
            self.default_vm_engine_stage_config()

            # STORAGE STAGE
            self.input_text(
                self.STORAGE_CONN,
                self.config_dict['nfs_ip'] + ':' + self.config_dict['nfs_dir'])
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 2000)

        self.prepare_env('nfs')
        time.sleep(15)
        check_deploy()

    # tier1_2
    def check_no_password_saved_in_setup_log(self):
        self.check_no_password_saved(self.config_dict['he_vm_pass'],
                                     self.config_dict['admin_pass'])

    # tier1_3
    def check_no_large_messages(self):
        size1 = self.host.execute(
            "ls -lnt /var/log/messages | awk '{print $5}'")
        print(size1)
        time.sleep(10)
        size2 = self.host.execute(
            "ls -lnt /var/log/messages | awk '{print $5}'")
        print(size2)
        if int(size2) - int(size1) > 800:
            self.fail()

    def deploy_on_registering_insights_server(self):
        username = self.config_dict['subscription_username']
        password = self.config_dict['subscription_password']
        try:
            sub_reg_ret = self.host.execute(
                "subscription-manager register --username={0} --password={1} --auto-attach".format(username, password), timeout=100)

            ins_reg_ret = self.host.execute("insights-client --register", timeout=100)

            if ("Status:       Subscribed" in sub_reg_ret.stdout) and ("Successfully registered" in ins_reg_ret.stdout):
                time.sleep(5)
                self.node_zero_default_deploy_process()
                he_ret = self.host.execute("hosted-engine --vm-status")

                if ('{"health": "good", "vm": "up", "detail": "Up"}' in he_ret.stdout):
                    ins_unreg_ret = self.host.execute("insights-client --unregister")
                    sub_unreg_ret = self.host.execute("subscription-manager unregister")
                    if ("Successfully unregistered" not in ins_unreg_ret.stdout) and (
                        "System has been unregistered." not in sub_unreg_ret.stdout):
                        raise RuntimeError("Unregister failed!")
        except:
            import traceback
            traceback.print_exc()
            self.fail()
        
    # tier1_4
    def add_additional_host_to_cluster_process(self):
        self.add_additional_host_to_cluster(
            self.config_dict['second_host'], self.config_dict['second_vm_fqdn'],
            self.config_dict['second_pass'], self.config_dict['he_vm_fqdn'],
            self.config_dict['admin_pass'])
        time.sleep(70)
        self.check_additional_host_socre(self.config_dict['second_host'],
                                         self.config_dict['second_pass'])
    
    # tier2_6
    def add_normal_host_to_cluster_process(self):
        self.add_normal_host_to_cluster(
            self.config_dict['normal_host'], self.config_dict['normal_host_fqdn'],
            self.config_dict['normal_pass'], self.config_dict['he_vm_fqdn'],
            self.config_dict['admin_pass'])
        time.sleep(70)
        # self.check_additional_host_socre(self.config_dict['normal_host'],
        #                                  self.config_dict['normal_pass'])

    # tier1_5
    def check_local_maintenance(self):
        self.put_host_to_local_maintenance()

    # tier1_6
    def check_hint_button_before_migration(self):
        self.assert_text_in_element(self.MIGRATION_HINT, 'Local maintenance cannot be set when running the engine VM, please migrate it from the engine first if needed.')

    def check_migrated_he(self):
        self.migrate_vms('HostedEngine', self.config_dict['second_vm_fqdn'], self.config_dict['he_vm_fqdn'], self.config_dict['admin_pass'])
        time.sleep(20)
        self.assert_text_in_element(self.VM_STATUS, 'down')
    
    def check_hint_button_after_migration(self):
        self.assert_element_invisible(self.MIGRATION_HINT)
    
    # tier1_7
    def check_remove_maintenance(self):
        self.remove_host_from_maintenance()

    # tier1_8
    def check_global_maintenance(self):
        self.put_cluster_to_global_maintenance()

    # tier1_9
    def reboot_hosted_engine_env(self):
        self.host.execute('reboot', raise_exception=False)
        time.sleep(1300)
        self.refresh()
        self.login(os.environ.get('USERNAME'), os.environ.get('PASSWD'))
        self.open_page()
        self.check_hosted_engine_status()
      

    # tier1_10
    def check_hosted_engine_status(self):
        self.assert_element_visible(self.ENGINE_UP_ICON)
        self.assert_element_visible(self.HE_RUNNING)

    # tier1_11
    def node_zero_rollback_deploy_process(self):
        def check_deploy():
            self.refresh()
            self.default_vm_engine_stage_config()

            #Check roll back history text.
            self.click(self.BACK_BUTTON)
            self.assert_text_visible("Execution completed successfully. Please proceed to the next step.", try_times=5)
            self.click(self.BACK_BUTTON)
            self.assertEqual(self.get_attribute(self.ADMIN_PASS, 'value'), self.config_dict['admin_pass'], 'Roll back history text wrong!')
            self.click(self.BACK_BUTTON)
            self.assertEqual(self.get_attribute(self.VM_FQDN, 'value'), self.config_dict['he_vm_fqdn'], 'Roll back history text wrong!')
            self.assertEqual(self.get_attribute(self.MAC_ADDRESS, 'value'), self.config_dict['he_vm_mac'], 'Roll back history text wrong!')
            self.assertEqual(self.get_attribute(self.ROOT_PASS,'value'), self.config_dict['he_vm_pass'], 'Roll back history text wrong!')
            for btn in range(3):
                self.click(self.NEXT_BUTTON)

            # STORAGE STAGE
            self.input_text(
                self.STORAGE_CONN,
                self.config_dict['nfs_ip'] + ':' + self.config_dict['nfs_dir'])
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 2000)

        self.prepare_env('nfs')
        time.sleep(15)
        check_deploy()

    # tier2_0
    def deploy_on_non_default_cockpit_port(self):
        self.node_zero_default_deploy_process()

    # tier2_1
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
            self.click(self.CLOSE_BUTTON, 2000)

        self.prepare_env('iscsi')
        check_deploy()

    # tier2_2
    def node_zero_fc_deploy_process(self):
        self.host.execute("hostnamectl set-hostname {}".format(self.config_dict['host_fc_hostname']),raise_exception=False)
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

    # tier2_3
    def node_zero_gluster_deploy_process(self):
        def check_deploy():
            self.default_vm_engine_stage_config()

            # STORAGE STAGE
            self.click(self.STORAGE_BUTTON)
            self.click(self.STORAGE_GLUSTERFS)
            self.input_text(
                self.STORAGE_CONN,
                list(self.config_dict['gluster_ips'].values())[0] + ':/' + self.config_dict['gluster_volume'])
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        self.prepare_env('gluster')
        check_deploy()

    # tier2_4
    def node_zero_static_v4_deploy_process(self):
        def check_deploy():
            # VM STAGE
            self.click(self.HE_START)
            time.sleep(150)
            self.input_text(self.VM_FQDN, self.config_dict['he_vm_fqdn'], 60)
            self.input_text(self.MAC_ADDRESS, self.config_dict['he_vm_mac'])
            self.click(self.NETWORK_DROPDOWN)
            self.click(self.NETWORK_STATIC)
            self.input_text(self.VM_IP, self.config_dict['he_vm_ip'])
            self.input_text(self.IP_PREFIX, self.config_dict['he_vm_ip_prefix'])
            self.input_text(self.DNS_SERVER, self.config_dict['dns_server'])
            self.input_text(self.ROOT_PASS, self.config_dict['he_vm_pass'])
            self.assert_text_in_element(self.VM_FQDN_VALIDATING_MSG, "Validating FQDN...")
            time.sleep(70)
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

    # tier2_5
    def hostedengine_redeploy_process(self):
        self.node_zero_default_deploy_process()

    # tier2_6
    def check_migrated_normal_host(self):
        try:
            self.migrate_vms('HostedEngine', self.config_dict['normal_host_fqdn'], 
                    self.config_dict['he_vm_fqdn'], self.config_dict['admin_pass'])
        except RuntimeError as e:
            print(e.__str__())
            if "Cannot migrate VM" in e.__str__():
                return True
            else:
                return False