import os
import yaml
import time
import datetime
import simplejson
import urllib2
import stat
import re
# import pytz
from seleniumlib import SeleniumTest
from utils.htmlparser import MyHTMLParser
from utils.machine import Machine
from utils.rhvmapi import RhevmAction
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


class CommonPages(SeleniumTest):
    """
    :avocado: disable
    """

    #R_MACHINE_ADDR="10.66.9.205"
    R_MACHINE_ADDR="10.73.130.125"
    WRONG_ADDR="1.2.3.4"
    R_MACHINE_USER="root"
    R_MACHINE_PWD="redhat"

    # RHSM_CUSTOM_URL="subscription.rhsm.stage.redhat.com"
    # RHSM_USER="shlei2"
    # RHSM_PWD="lsystc571998"

    # NFS_SERVER_ADDR="10.66.10.132"
    # SERVER_PATH="/home/shiyilei/nfs"
    # MOUNT_POINT="/root/mnt"

    LOGIN_ERROR_MESSAGE="//*[@id='login-error-message']"

    OTHER_OPTION="//*[@id='show-other-login-options']"
    SERVER_FIELD="//*[@id='server-field']"

    SLEEP_TIME = 5
    OVIRT_DASHBOARD_FRAME_NAME = "/dashboard"
    LOCALHOST_LINK = "//*[@id='host-nav-link']/span[1]"
    DASHBOARD_LINK = "//*[@id='host-apps']/nav/section[1]/ul/li[2]/span/a"
    OVIRT_HOSTEDENGINE_FRAME_NAME = "/ovirt-dashboard"

    #add and delete remote host
    DOMAIN_BUTTON="//*[@id='pf-toggle-id-58']"
    ADD_SERVER_BUTTON="//*[@id='page-sidebar']/div/div[2]/button"
    INPUT_MACHINE_ADDRESS="//*[@id='add-machine-address']"
    ADD_HOST_BUTTON="//*[@id='hosts_setup_server_dialog']/div/div/div[2]/div/button[1]"
    CONNECT_BUTTON="//*[@id='hosts_setup_server_dialog']/div/div/div[3]/button[1]"
    INPUT_REMOTE_USER="//*[@id='login-custom-user']"
    INPUT_REMOTE_PASSWORD="//*[@id='login-custom-password']"

    EDITE_SERVER="//*[@id='page-sidebar']/div/div[2]/button[1]"
    DELETE_SERVER="//*[@id='page-sidebar']/div/nav/section/ul/li[2]/span/div/button[2]"
    
    #subscription
    NETWORK_INFO_LINK="//*[@id='content']/div/div/div[1]/table/tbody[4]/tr[1]/td[2]/a"
    SUBSCRIPTION_LINK="//*[@id='host-apps']/nav/section[3]/ul/li[4]/span/a"
    
    SUBSCRIPTION_FRAME_NAME="/subscriptions"
    REGIST_BUTTON="//*[@id='app']/div/div/button"
    CHOOSE_URL_BUTTON="//*[@id='subscription-register-url']/button"
    CUSTOM_URL_BUTTON="//*[@id='subscription-register-url']/ul/li[2]/a"
    CUSTOM_URL_TEXT="//*[@id='subscription-register-url-custom']"
    SUBSCRIPTION_USER_TEXT="//*[@id='subscription-register-username']"
    SUBSCRIPTION_ORGANIZATION_TEXT="//*[@id='subscription-register-org']"
    SUBSCRIPTION_PWD_TEXT="//*[@id='subscription-register-password']"
    REGIST_COMMIT_BUTTON="//*[@id='register_dialog']/div/div[3]/button[1]"
    
    DETAIL_BUTTON = "//*[@id='app']/div/div[2]/div[2]/div[1]/div[1]/div[1]/span"
    
    DETALI_PRODUCT_NAME = "//*[@id='app']/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/dl/dd[1]"
    
    DETAIL_PRODUCT_ID = "//*[@id=app']/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/dl/dd[2]"
    DETAIL_PRODUCT_VERSION = "//*[@id='app']/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/dl/dd[3]"
    DETAIL_PRODUCT_STATUS = "//*[@id='app']/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/dl/dd[5]"
    ORGANIZATION_TEXT= "//*[@id='subscription-register-org']"
    KEY_TEXT="//*[@id='subscription-register-key']"

    #add nfs
    STORAGE_LINK="//*[@id='host-apps']/nav/section[2]/ul/li[3]/span/a"
    STORAGE_FRAME_NAME="/storage"
    ADD_NFS_BUTTON="//*[@id='nfs-mounts']/div[1]/div/button"
    NFS_SERVER_ADDR_TEXT="//*[@id='pf-modal-part-2']/form/div[1]/input"
    SERVER_PATH_TEXT="//*[@id='pf-select-toggle-id-0-select-typeahead']"
    NFS_PATHS=""
    MOUNT_POINT_TEXT="//*[@id='dialog']/div/div/div[2]/form/div[3]/input"
    NFS_ADD_BUTTON="//*[@id='dialog']/div/div/div[3]/button[1]"

    NFS_SERVER_DETAIL_BUTTON="//*[@id='nfs-mounts']/table/tbody/tr/td[1]"
    DELETE_NFS_SERVER_BUTTON="//*[@id='detail-header']/div/div[1]/span/button[3]"
    NFS_UNMOUNT_BUTTON="//*[@id='detail-header']/div/div[1]/span/button[1]"
    NFS_SIZE_FIELD="#detail-header > div > div.panel-body > div"
    
    NFS_SIZE_PROGRESS="#pf-15846295830663u3ki41vij2 > div.pf-c-progress__bar > div"
    NFS_STATUS="//*[@id='pf-15846295830663u3ki41vij2']/div[2]/span"

    #system status
    CPU_STATUS="//*[@id='current-metrics-card-cpu']/div[1]"
    MEMORY_LINK="//*[@id='dashboard']/div[1]/div/ul/li[2]/a"
    MEMORY_STATUS="//*[@id='app']/div/main/section[1]/div/article[2]/div[1]"
    NETWORK_LINK="//*[@id='dashboard']/div[1]/div/ul/li[3]/a"
    NETWORK_STATUS="//*[@id='app']/div/main/section[1]/div/article[4]/div[1]"
    DISK_LINK="//*[@id='dashboard']/div[1]/div/ul/li[4]/a"
    DISK_STATUS="//*[@id='app']/div/main/section[1]/div/article[3]/div[1]"

    #config hostname
    SYSTEM_FRAME_LINK="//*[@id='host-apps']/nav/section[2]/ul/li[1]/span/a"
    SYSTEM_FRAME_NAME="/system"
    HOSTNAME_BUTTON="//*[@id='system_information_hostname_button']"
    HOST_INFO_TEXT="//*[@id='system_information_hostname_text']"
    PRETTY_HOSTNAME_TEXT="//*[@id='sich-pretty-hostname']"
    REAL_HOSTNAME_TEXT="//*[@id='sich-hostname']"
    HOSTNAME_APPLY_BUTTON="//*[@id='sich-apply-button']"

    #config timezone
    TIME_LINK="//*[@id='system_information_systime_button']"
    # TIMEZONE_TEXT="//*[@id='systime-timezonesundefined']"
    TIMEZONE_REMOVER="//*[@id='systime-timezonesundefined']//parent::*/span"
    TIMEZONE_DROPDOWN="//*[@id='systime-timezonesundefined']//parent::*/span"
    TIMEZONE_ITEM="//*[@id='systime-timezonesundefined']//parent::*/ul/li[1]"
    TIMEZONE_APPLY_BUTTON="//*[@id='system_information_change_systime']/div/div/div[3]/button[1]"
    
    TIME_SET_DROPDOWN="//*[@id='change_systime']/button"
    TIME_SET_MANUALLY="//*[@id='change_systime']/ul/li[1]/a"
    TIME_MIN_TEXT="//*[@id='systime-time-minutes']"

    #restart node
    RESTART_BUTTON="//*[@id='restart-button']"
    LEAVE_MESSAGE_TEXT="//*[@id='shutdown-dialog']/div/div/div[2]/textarea"
    RESTART_APPLY_BUTTON="//*[@id='shutdown-dialog']/div/div/div[3]/button[2]"
    RECONNECT_BUTTON="//*[@id='machine-reconnect']"

    #change the performance profile
    PROFILE_LINK="//*[@id='tuned-status-button']"
    DESKTOP_OPTION="button.list-group-item:nth-child(4)"
    PROFILE_APPLY_BUTTON=".apply"

    #kernel dump
    KD_LINK="//*[@id='sidebar-tools']/li[2]/a"
    #//*[@id="sidebar-tools"]/li[3]/a //*[@id="sidebar-tools"]/li[2]/a //*[@id="sidebar-tools"]/li[3]
    HINT="//*[@id='app']/div/form/div[2]/a/span"
    KDUMP_SERVICE_STATUS="//*[@id='app']/div/form/div[1]/a/span"
    BTN_TEST_CONFIGURATION="//*[@id='app']/div/form/div[2]/button"
    CRASH_SYSTEM_BUTTON="body > div:nth-child(3) > div.in.modal > div > div > div.modal-footer > button.btn.btn-danger.apply" 
    
    KD_FRAME_NAME="/kdump"
    KD_SERVICE_LINK="//*[@id='app']/div/form/div[1]/a/span"
    SERVICES_LINK="//*[@id='sidebar-menu']/li[7]/a/span"
    SERVICE_FRAME_NAME="/system/services"
    SERVICE_SEARCHER="//*[@id='services-text-filter']"
    KD_SERVICE_LINK="//*[@id='services-list']/div/table/tbody/tr/td[1]"
    STOP_START_BUTTON="//*[@id='service-details']/main/section[2]/div/span/label/span"
    KD_STATUS_INFO="//*[@id='statuses']/div/span[2]"
    KD_STATUS_INFO2=".status-running > span:nth-child(2)"
    KD_RESTART_BUTTON="//*[@id='service-unit-action']/button[1]"
    KD_DISABLE_BUTTON="//*[@id='service-file-action']/button[1]"
    KD_ENABLE_TEXT="//*[@id='service-unit']/div/div[2]/div[1]/table/tbody/tr[3]/td[2]"

    #check system logs
    LOGS_LINK="//*[@id='host-apps']/nav/section[2]/ul/li[2]/span/a"
    LOGS_FRAME_NAME="/system/logs"
    LOGS_DURATION_BUTTON="//*[@id='log-filters']"
    # RECENT_LOGS="//*[@id='journal-current-day-menu']/ul/li[1]/a"
    # CURRENT_BOOT="//*[@id='journal-current-day-menu']/ul/li[2]/a"
    LAST_ONE_DAY="//*[@id='logs-predefined-filters']/li[3]/a"
    LAST_SEVEN_DAYS="//*[@id='logs-predefined-filters']/li[4]/a"
    LOGS_LOAD_EARLIER="//*[@id='journal-load-earlier']"
    LOG_INFO="//*[@id='journal-box']/div[1]/div[2]/span"
    LOGS_FILTER="//*[@id='journal-prio-menu']/button"
    LOGS_EVERYTHING="//*[@id='prio-lists']/li[1]/a"
    LOGS_WARNING_ICON="//*[@id='journal-box']/div[1]/div[2]/div[1]"

    #create new account
    ACCOUNT_LINK="//*[@id='host-apps']/nav/section[2]/ul/li[5]/span/a"
    ACCOUNT_FRAME_NAME="/users"
    CREATE_NEW_ACCOUNT_BUTTON="//*[@id='accounts-create']"
    FULL_NAME_TEXT="//*[@id='accounts-create-real-name']"
    PASSWORD_TEXT="//*[@id='accounts-create-pw1']"
    CONFIRM_TEXT="//*[@id='accounts-create-pw2']"
    CREATE_BUTTON="//*[@id='accounts-create-dialog']/div/div/div[3]/button[1]"
    ACCOUNT_INFO="//*[@id='accounts-list']/li[2]"

    ROOT_BUTTON="//*[@id='navbar-dropdown']"
    LOGOUT_BUTTON="//*[@id='go-logout']"
    LOGIN_USERNAME_TEXT="//*[@id='login-user-input']"
    LOGIN_PWD_TEXT="//*[@id='login-password-input']"
    LOGIN_BUTTON="//*[@id='login-button']"

    #terminal function
    TERMINAL_LINK="//*[@id='host-apps']/nav/section[3]/ul/li[5]/span/a"
    
    TERMINAL_FRAME_NAME="/system/terminal"
    TERMINAL_ADMIN="//*[@id='terminal']/div/div[2]/div/div/div[1]/div[1]/div[5]"
    CONMMAND_LINE="/html/body/div/div/div[2]/div/div/div[1]/div[1]/div[7]"
    
    SSH_HOST_KEY_LINK="//*[@id='content']/div/div/div[1]/table/tbody[5]/tr/td[2]/a"
    SSH_HOST_KEY_COTENT="//*[@id='content']/div/div/div[1]/table/tbody[5]/tr/td[2]/div/div/div/div/div[2]/div"

    #check diagnostic report
    DIAGNOSTIC_REPORT_LINK="//*[@id='host-apps']/nav/section[3]/ul/li[1]/span/a"
    DIAGNOSTIC_REPORT_FRAME="/sosreport"
    CREATE_REPORT_BUTTON="//button[text()='Create Report']"
    REPORT_DIALOG="//*[@id='sos']/div"
    REPORT_DOWNLOAD_BUTTON="#sos-download > button"
    
    #check_selinux_policy
    SELINUX_LINK="//*[@id='host-apps']/nav/section[3]/ul/li[3]/span/a"
    SELINUX_FRAME="/selinux/setroubleshoot"
    SWITCH_BUTTON="#app > div > div > div > label > span"

    #check udisks
    SERVICE_LINK="//*[@id='host-apps']/nav/section[2]/ul/li[6]/span/a"
    
    FILTER_INPUT_TEXT="//*[@id='services-text-filter']"
    UDISKS_STATUS_TEXT="//*[@id='udisks2.service']/div/div[2]/span[1]"

    #system infomation
    SYSTEM_USAGE_LINK="//*[@id='overview']/div/main/section[2]/div[2]/article[2]/div[3]/a"

    def setUp(self):
        case_name = self._testMethodName
        config = self.get_data('cockpit_common.yml')
        self.config_dict = yaml.load(open(config))
        
        if 'firefox' in case_name.split('_'):
            os.environ['BROWSER']='firefox'
        if 'chrome' in case_name.split('_'):
            os.environ['BROWSER']='chrome'
        if 'login' in case_name.split('_'):
            os.environ['USERNAME']='invalid_user'
            os.environ['PASSWD']='invalid_pwd'
        super(CommonPages,self).setUp()

    def open_page(self):

        # self.click(self.DASHBOARD_LINK)

        # time.sleep(1)
        # self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)
        pass
    
    def check_firefox_login(self):
        self.assertEqual(self.get_text(self.LOGIN_ERROR_MESSAGE),"Wrong user name or password")
        time.sleep(3)
        config_dict = yaml.load(open('./config.yml'))
        os.environ['USERNAME'] = config_dict['host_user']
        os.environ['PASSWD'] = config_dict['host_pass']

        host_string = os.environ.get('HOST_STRING')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')

        host = Machine(host_string, username, passwd)

        self.login(username, passwd)
        time.sleep(5)
        cmd = 'systemctl status cockpit |grep running'
        output = host.execute(cmd).stdout
        print(output)
        result = re.search("running",output)
        self.assertNotEqual(result, None)
        
    def check_chrome_login(self):
        self.check_firefox_login()
        
    def login_remote_machine(self):
        time.sleep(5)
        self.click(self.OTHER_OPTION)
        self.input_text(self.SERVER_FIELD,self.R_MACHINE_ADDR)
        self.login(self.R_MACHINE_USER,self.R_MACHINE_PWD)
        time.sleep(2)
        actual_s = self.get_current_url().split('=')[-1]
        expect_s = self.R_MACHINE_ADDR + '/system'
        self.assertEqual(actual_s,expect_s)

    def login_wrong_remote_machine(self):
        time.sleep(2)
        self.click(self.OTHER_OPTION)
        self.input_text(self.SERVER_FIELD,self.WRONG_ADDR)
        self.login(self.R_MACHINE_USER,self.R_MACHINE_PWD)
        time.sleep(15)
        self.assertEqual(self.get_text(self.LOGIN_ERROR_MESSAGE),"Unable to connect to that address")

        
    def add_remote_host(self):
        self.click(self.DOMAIN_BUTTON)
        self.click(self.ADD_SERVER_BUTTON)
        time.sleep(5)
        self.input_text(self.INPUT_MACHINE_ADDRESS,self.R_MACHINE_ADDR)
        # self.input_text(self.INPUT_REMOTE_USER,self.R_MACHINE_USER)
        self.click(self.ADD_HOST_BUTTON)
        time.sleep(3)
        self.click(self.CONNECT_BUTTON)
        time.sleep(3)
        self.input_text(self.INPUT_REMOTE_PASSWORD,self.R_MACHINE_PWD)
        self.click(self.CONNECT_BUTTON)
        self.assert_element_visible("//*[@id='page-sidebar']/div/nav/section/ul/li[2]/span/a/span")

    def delete_remote_host(self):
        self.click(self.DOMAIN_BUTTON)

        self.click(self.EDITE_SERVER)
        time.sleep(2)
        self.click(self.DELETE_SERVER)
        time.sleep(2)
        self.assert_element_invisible(self.EDITE_SERVER)
    
    def subscription_to_rhsm(self):
        self.host.execute("subscription-manager config --server.hostname=subscription.rhsm.stage.redhat.com")
        self.click(self.SUBSCRIPTION_LINK)
        time.sleep(5)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        time.sleep(2)
        self.click(self.REGIST_BUTTON)
        self.input_text(self.SUBSCRIPTION_USER_TEXT, self.config_dict['subscription_username'])
        self.input_text(self.SUBSCRIPTION_PWD_TEXT, self.config_dict['subscription_password'])
        self.input_text(self.SUBSCRIPTION_ORGANIZATION_TEXT, "12801563")
        time.sleep(2)
        self.click(self.REGIST_COMMIT_BUTTON)
        time.sleep(60)
        self.refresh()
        time.sleep(10)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        self.assert_text_in_element("//*[@id='app']/div/div/label", "Status: Current")
        self.click(self.DETAIL_BUTTON)
        time.sleep(2)
        self.assert_text_in_element(self.DETALI_PRODUCT_NAME, "Red Hat Virtualization Host")
        self.assert_text_in_element(self.DETAIL_PRODUCT_VERSION, "4")
        self.assert_text_in_element(self.DETAIL_PRODUCT_STATUS, "Subscribed")

    def check_packages_installation(self):
        self.host.execute("subscription-manager config --rhsm.baseurl=https://cdn.stage.redhat.com")
        self.host.execute("subscription-manager repos --disable=*")
        self.host.execute("subscription-manager repos --enable=%s" %self.config_dict['subscription_repos'])
        
        sub_pkgs = self.config_dict['subscription_packages']
        # for pkg in sub_pkgs[:-1]:
        #     ret = self.host.execute("yum install -y %s" % pkg, timeout=200)
        #     self.assertTrue('Complete!' in ret.stdout)
        self.assertTrue('rhvm-appliance' in self.host.execute("yum search %s" %sub_pkgs[-1]))
        ret = self.host.execute("yum search vdsm-hook*", timeout=200)
        self.assertTrue('vdsm-hook-checkips' in ret.stdout)
        self.assertTrue('vdsm-hook-cpuflags' in ret.stdout)
        self.assertTrue('vdsm-hook-ethtool-options' in ret.stdout)
        self.assertTrue('vdsm-hook-extra-ipv4-addrs' in ret.stdout)
        self.assertTrue('vdsm-hook-fcoe' in ret.stdout)
        self.assertTrue('vdsm-hook-localdisk' in ret.stdout)
        self.assertTrue('vdsm-hook-nestedvt' in ret.stdout)
        self.assertTrue('vdsm-hook-openstacknet' in ret.stdout)
        self.assertTrue('vdsm-hook-vhostmd' in ret.stdout)
        self.assertTrue('vdsm-hook-vmfex-dev' in ret.stdout)


    def add_nfs_storage(self):
        self.click(self.STORAGE_LINK)
        self.switch_to_frame(self.STORAGE_FRAME_NAME)
        time.sleep(2)
        self.click(self.ADD_NFS_BUTTON)
        time.sleep(2)
        self.input_text(self.NFS_SERVER_ADDR_TEXT, self.config_dict['nfs_ip'])
        time.sleep(1)
        self.input_text(self.SERVER_PATH_TEXT, self.config_dict['nfs_dir'])
        time.sleep(1)
        self.click('//*[@id="pf-modal-part-2"]/form/label[3]')
        self.input_text(self.MOUNT_POINT_TEXT, self.config_dict['nfs_mount_point'])
        time.sleep(1)
        self.click(self.NFS_ADD_BUTTON)
        time.sleep(3)
        self.assert_element_visible("//*[@id='nfs-mounts']/table/tbody/tr")
        self.click(self.NFS_SERVER_DETAIL_BUTTON)
        time.sleep(3)
        self.click(self.DELETE_NFS_SERVER_BUTTON)
        time.sleep(2)
        self.assert_element_invisible(self.NFS_SERVER_DETAIL_BUTTON)
        self.assert_element_invisible("//*[@id='nfs-mounts']/table/tbody/tr")
    
    def system__dynamic_status(self):
        self.click(self.SYSTEM_FRAME_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        self.click(self.SYSTEM_USAGE_LINK)
        self.assert_text_in_element(self.CPU_STATUS,"CPU")
        self.assert_text_in_element(self.MEMORY_STATUS,"Memory")
        self.assert_text_in_element(self.NETWORK_STATUS,"Network")
        self.assert_text_in_element(self.DISK_STATUS,"Disks")
  
    def config_hostname(self):
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        self.click(self.HOSTNAME_BUTTON)

        self.input_text(self.PRETTY_HOSTNAME_TEXT,"test")
        time.sleep(1)
        self.input_text(self.REAL_HOSTNAME_TEXT,"test.redhat.com")
        time.sleep(1)
        self.click(self.HOSTNAME_APPLY_BUTTON)
        time.sleep(2)

        self.assert_text_in_element(self.HOST_INFO_TEXT,"test (test.redhat.com)")

        cmd = 'hostname'
        output = self.host.execute(cmd).stdout
        result = re.match("test.redhat.com",output)
        self.assertNotEqual(result, None)

    def config_timezone(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SYSTEM_FRAME_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)

        self.click(self.TIME_LINK)
        self.click(self.TIMEZONE_REMOVER)
        self.click(self.TIMEZONE_DROPDOWN)
        time.sleep(1)
        self.click(self.TIMEZONE_ITEM)
        time.sleep(1)
        self.click(self.TIMEZONE_APPLY_BUTTON)
        time.sleep(1)
        self.refresh()
        time.sleep(5)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        actual_now = self.get_text(self.TIME_LINK)
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        respect_now = utc_now.astimezone(pytz.timezone("Africa/Abidjan")).strftime("%Y-%m-%d %H:%M")
        self.assertEqual(actual_now,respect_now)

    def config_time_manually(self):
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        self.click(self.TIME_LINK)
        self.input_text(self.TIME_MIN_TEXT,"00")
        self.click(self.TIMEZONE_APPLY_BUTTON)
        time.sleep(2)
        self.refresh()
        time.sleep(5)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        actual_now = self.get_text(self.TIME_LINK).split(':')[-1]
        self.assertEqual(actual_now,"00 PM")
    
    def restart_node(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SYSTEM_FRAME_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        time.sleep(2)
        self.click(self.RESTART_BUTTON)
        self.input_text(self.LEAVE_MESSAGE_TEXT,"GOODBYE!!!")
        time.sleep(2)
        self.click(self.RESTART_APPLY_BUTTON)
        time.sleep(70)
        self.switch_to_default_content()
        self.assert_element_visible("//*[@id='content']/div")

        time.sleep(300)
        self.click(self.RECONNECT_BUTTON)
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        self.login(username, passwd)
        time.sleep(2)
        self.assert_frame_available("/system")

    def change_performance_profile(self):
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)

        self.click(self.PROFILE_LINK)
        time.sleep(2)
        self.click(self.DESKTOP_OPTION)
        self.click(self.PROFILE_APPLY_BUTTON)

        cmd = 'tuned-adm active'
        output = self.host.execute(cmd).stdout
        result = re.search("desktop",output)
        self.assertNotEqual(result, None)
    
    def check_service_status(self):
        self.click(self.SERVICE_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SERVICE_FRAME_NAME)
        self.input_text(self.FILTER_INPUT_TEXT,"kdump")
        time.sleep(3)
        self.click("//*[@id='kdump.service']/div/div[1]/div[1]")

        self.click(self.STOP_START_BUTTON)
        time.sleep(10)
        self.assert_text_in_element(self.KD_STATUS_INFO,"Disabled")
        self.click(self.STOP_START_BUTTON)
        time.sleep(8)
        self.assert_text_in_element(self.KD_STATUS_INFO2,"Running")
    
    def check_file_system_list(self):
        self.click(self.STORAGE_LINK)
        time.sleep(5)
        self.switch_to_frame(self.STORAGE_FRAME_NAME)
        
        self.assert_text_in_element("//*[@id='mounts']/table/tbody/tr[8]/td[2]","/boot")
        # self.click("//*[@id='storage_mounts']/tr[1]/td[2]/div")
        time.sleep(1)
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[2]/tr[1]/td[2]/span","1 GiB")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[5]/tr[1]/th","root")

        #tmp
        self.click("#mounts > table > tbody > tr:nth-child(3) > td:nth-child(2)")
        self.assert_text_in_element("//*[@id='detail-content']/section/table/tbody/tr[1]/td[2]/span","1 GiB")
        self.click("#storage-detail > div.col-md-12 > ol > li:nth-child(1) > button")
        #var
        self.click("#mounts > table > tbody > tr:nth-child(4) > td:nth-child(2)")
        self.assert_text_in_element("//*[@id='detail-content']/section/table/tbody/tr[1]/td[2]/span","15 GiB")
        self.click("#storage-detail > div.col-md-12 > ol > li:nth-child(1) > button")
        #var_crash
        self.click("#mounts > table > tbody > tr:nth-child(5) > td:nth-child(2)")
        self.assert_text_in_element("//*[@id='detail-content']/section/table/tbody/tr[1]/td[2]/span","10 GiB")
        self.click("#storage-detail > div.col-md-12 > ol > li:nth-child(1) > button")
        #var_log
        self.click("#mounts > table > tbody > tr:nth-child(6) > td:nth-child(2)")
        self.assert_text_in_element("//*[@id='detail-content']/section/table/tbody/tr[1]/td[2]/span","8 GiB")
        self.click("#storage-detail > div.col-md-12 > ol > li:nth-child(1) > button")
        #var_log_audit
        self.click("#mounts > table > tbody > tr:nth-child(7) > td:nth-child(2)")
        self.assert_text_in_element("//*[@id='detail-content']/section/table/tbody/tr[1]/td[2]/span","2 GiB")
        self.click("#storage-detail > div.col-md-12 > ol > li:nth-child(1) > button")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[6]/tr[1]/th","/tmp")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[7]/tr[1]/td[2]/span","15 GiB")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[7]/tr[1]/th","/var")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[8]/tr[1]/td[2]/span","10 GiB")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[8]/tr[1]/th","/var_crash")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[9]/tr[1]/td[2]/span","8 GiB")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[9]/tr[1]/th","/var_log")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[10]/tr[1]/td[2]/span","2 GiB")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[10]/tr[1]/th","/var_log_audit")
        # self.assert_text_in_element("//*[@id='detail-content']/table/tbody[11]/tr[1]/th","swap")
    
    def modify_nfs_storage(self):
        self.click(self.STORAGE_LINK)
        self.switch_to_frame(self.STORAGE_FRAME_NAME)
        self.click(self.ADD_NFS_BUTTON)
        time.sleep(2)
        self.input_text(self.NFS_SERVER_ADDR_TEXT, self.config_dict['nfs_ip'])
        time.sleep(1)
        self.input_text(self.SERVER_PATH_TEXT, self.config_dict['nfs_dir'])
        time.sleep(1)
        self.input_text(self.MOUNT_POINT_TEXT, self.config_dict['nfs_mount_point'])
        time.sleep(1)
        self.click(self.NFS_ADD_BUTTON)
        time.sleep(3)
        self.click(self.NFS_SERVER_DETAIL_BUTTON)
        time.sleep(2)
        self.click(self.NFS_UNMOUNT_BUTTON)
        time.sleep(1)
        self.assert_text_in_element(self.NFS_SIZE_FIELD,"--")
        self.click(self.NFS_UNMOUNT_BUTTON)
        time.sleep(2)
        #self.assert_element_visible(self.NFS_SIZE_PROGRESS)
        #self.assert_text_visible(self.NFS_STATUS)
        self.click(self.DELETE_NFS_SERVER_BUTTON)
        time.sleep(2)
        self.assert_element_invisible("//*[@id='nfs-mounts']/table/tbody/tr")
    
    def check_the_logs(self):
        self.click(self.LOGS_LINK)
        self.switch_to_frame(self.LOGS_FRAME_NAME)

        self.click(self.LOGS_DURATION_BUTTON)
        time.sleep(1)
        self.click(self.LAST_ONE_DAY)
        time.sleep(3)
        self.assert_element_visible(self.LOG_INFO)
        self.assert_element_visible(self.LOGS_WARNING_ICON)
        self.click(self.LOGS_DURATION_BUTTON)
        time.sleep(1)
        self.click(self.LAST_SEVEN_DAYS)
        time.sleep(3)
        self.assert_element_visible(self.LOG_INFO)

    def create_new_account(self):
        self.click(self.ACCOUNT_LINK)
        time.sleep(1)
        self.switch_to_frame(self.ACCOUNT_FRAME_NAME)

        self.click(self.CREATE_NEW_ACCOUNT_BUTTON)
        time.sleep(3)
        self.input_text(self.FULL_NAME_TEXT,"user_a")
        self.input_text(self.PASSWORD_TEXT,"shleishlei123!")
        self.input_text(self.CONFIRM_TEXT,"shleishlei123!")
        self.click(self.CREATE_BUTTON)
        time.sleep(5)
        self.assert_element_visible(self.ACCOUNT_INFO)

        self.switch_to_default_content()
        self.click(self.ROOT_BUTTON)
        self.click(self.LOGOUT_BUTTON)
        time.sleep(1)
        self.input_text(self.LOGIN_USERNAME_TEXT,"user_a")
        self.input_text(self.LOGIN_PWD_TEXT,"shleishlei123!")
        self.click(self.LOGIN_BUTTON)
        time.sleep(3)
        self.assert_frame_available("/users")
    

    def check_terminal(self):
        self.click(self.TERMINAL_LINK)
        time.sleep(1)
        self.switch_to_frame(self.TERMINAL_FRAME_NAME)
        time.sleep(3)
        self.click(self.CONMMAND_LINE)
        self.input_text(self.CONMMAND_LINE," nodectl check\r\n",False)
        time.sleep(5)
        self.assert_text_in_element("//*[@id='the-terminal']/div/div/div[1]/div[1]/div[9]","Status: OK")

    def go_to_network_page(self):
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.click(self.NETWORK_INFO_LINK)
        self.switch_to_default_content()
        time.sleep(3)
        self.assert_frame_available("/network")
    
    def go_to_logs_page(self):
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.click(self.LOGS_LINK)
        self.switch_to_default_content()
        time.sleep(3)
        self.assert_frame_available(self.LOGS_FRAME_NAME)
    
    def go_to_storage_page(self):
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.click(self.STORAGE_LINK)
        self.switch_to_default_content()
        time.sleep(3)
        self.assert_frame_available(self.STORAGE_FRAME_NAME)

    def create_dignostic_report(self):
        self.click(self.DIAGNOSTIC_REPORT_LINK)
        time.sleep(1)
        self.switch_to_frame(self.DIAGNOSTIC_REPORT_FRAME)
        time.sleep(3)
        self.click(self.CREATE_REPORT_BUTTON)
        self.assert_element_visible(self.REPORT_DIALOG)
        time.sleep(100)
        self.assert_element_visible(self.REPORT_DOWNLOAD_BUTTON)
        self.click(self.REPORT_DOWNLOAD_BUTTON)
        time.sleep(3)
    
    def check_selinux_policy(self):
        self.click(self.SELINUX_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SELINUX_FRAME)

        cmd = 'getenforce'
        output = self.host.execute(cmd).stdout
        result = re.match("Enforcing",output)
        self.assertNotEqual(result, None)

        time.sleep(3)
        self.click(self.SWITCH_BUTTON)
        time.sleep(5)

        output = self.host.execute(cmd).stdout
        result = re.match("Permissive",output)
        self.assertNotEqual(result, None)

        cmd2="setenforce 0"
        output2 = self.host.execute(cmd2).stdout
        self.refresh()
        time.sleep(5)

        cmd3="setenforce 1"
        output3 = self.host.execute(cmd3).stdout
        self.refresh()
        time.sleep(5)

    def check_udisks_service(self):
        cmd = 'rpm -qa|grep udisks2'
        output = self.host.execute(cmd).stdout
        result = re.search("udisks2",output)
        self.assertNotEqual(result, None)

        self.click(self.SERVICE_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SERVICE_FRAME_NAME)
        self.input_text(self.FILTER_INPUT_TEXT,"udisks")
        time.sleep(3)
        self.assert_text_in_element(self.UDISKS_STATUS_TEXT,"Running")

        cmd = "systemctl status udisks2 |grep 'running' && systemctl status udisks2 |grep PID"
        output = self.host.execute(cmd).stdout
        start_point=re.search("PID:",output).end()+1
        end_point=re.search("(udisksd)",output).start()-2
        print(output[start_point:end_point])
        process_id=output[start_point:end_point]
        cmd='for i in {1..100}; do lsof -p'+' {} | wc -l 1>> /tmp/files; sleep 5; done'.format(process_id)
        output = self.host.execute(cmd,timeout=510).stdout
        self.assertEqual(output,'')
    
    def check_kernel_dump_service(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.KD_LINK)
        self.switch_to_frame(self.KD_FRAME_NAME)

        time.sleep(3)
        self.assert_text_in_element(self.KDUMP_SERVICE_STATUS, 'Service is running')
        
        kdump_service_status = self.host.execute("systemctl stop kdump").stdout
        time.sleep(3)
        self.assert_text_in_element(self.KDUMP_SERVICE_STATUS, 'Service is stopped')
        self.assertTrue('disabled' in self.get_attribute(self.BTN_TEST_CONFIGURATION, 'class'))
        kdump_service_status = self.host.execute("systemctl start kdump").stdout
        time.sleep(5)
        self.assert_text_in_element(self.KDUMP_SERVICE_STATUS, 'Service is running')
        self.assertFalse('disabled' in self.get_attribute(self.BTN_TEST_CONFIGURATION, 'class'))
        
        self.hover_and_click(self.HINT)
        self.assert_element_visible("//*[@id='tip-test-info']")

    def check_appliance_like(self, s_app_like):
        appliance_like_list = s_app_like.split(': ')
        print(appliance_like_list)
        self.assertEqual(appliance_like_list[0], "Admin Console")
        addr_l = appliance_like_list[-1].split(' ')
        address_list = []
        for i in range(len(addr_l)):
            if addr_l[i] != 'or':
                address_list.append(addr_l[i])
        
        re_ipv4 = "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        re_ipv6 = "^(?:[a-f0-9]{1,4}:){7}[a-f0-9]{1,4}$"
        for addr in address_list:
            if len(addr) <= len('http://255.255.255.255:9090'):
                self.assertNotEqual(re.match(re_ipv4, addr[8:-6]), None)
            else:
                self.assertNotEqual(re.match(re_ipv6, addr[8:-6]), None)

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

    def goto_terminal_check_appliance(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.TERMINAL_LINK)
        time.sleep(2)
        self.switch_to_frame(self.TERMINAL_FRAME_NAME)
        appliance_like = self.get_text(self.TERMINAL_ADMIN)
        self.check_appliance_like(appliance_like)  

    def add_host_rhvm(self, host_ip,host_name,host_pass,rhvm_fqdn):
        rhvm = RhevmAction(rhvm_fqdn)
        rhvm.add_host(host_ip, host_name, host_pass, "Default")
        self.wait_host_up(rhvm, host_name, 'up')

    def check_appliance_like_text(self):
        host_ip = os.environ.get('HOST_STRING')
        host_name = self.host.execute("hostname").stdout
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        rhvm_fqdn = self.config_dict['rhvm_fqdn']

        self.goto_terminal_check_appliance()
        self.add_host_rhvm(host_ip,host_name,passwd,rhvm_fqdn)
        time.sleep(150)
        self.host.execute("reboot",raise_exception=False)
        time.sleep(400)
        self.refresh()
        self.login(username, passwd)
        time.sleep(2)
        self.click(self.TERMINAL_LINK)
        time.sleep(2)
        self.switch_to_frame(self.TERMINAL_FRAME_NAME)
        appliance_like = self.get_text(self.TERMINAL_ADMIN)
        print(appliance_like)
        self.check_appliance_like(appliance_like) 
    
    def check_password_is_encrypted_in_log(self):
        try:
            self.host.get_file('/var/log/rhsm/rhsm.log','./rhsm.log')
            pwd=self.config_dict['subscription_password']
            with open('./rhsm.log') as config_file:
                while True:
                    content=config_file.readline()
                    if content:
                        outcome=re.search(pwd,content)
                        self.assertEqual(outcome,None)
                    else:
                        break
            os.remove('./rhsm.log')
        except Exception as e:
            pass
    
    def capture_vmcore_at_local(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)

        self.click(self.KD_LINK)
        time.sleep(2)
        self.switch_to_frame(self.KD_FRAME_NAME)
        time.sleep(1)
        self.click(self.BTN_TEST_CONFIGURATION)
        self.click(self.CRASH_SYSTEM_BUTTON)
        time.sleep(330)

        cmd = 'ls /var/crash'
        output = self.host.execute(cmd).stdout
        self.assertNotEqual(output.split(' ')[0], None)
        res_date = '-'.join(output.split(' ')[0].split(':')[0].split('-')[-4:-1])
        des_date = datetime.date.today().__str__()
        self.assertEqual(res_date, des_date)
    
    def subscription_with_key_and_organization(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SUBSCRIPTION_LINK)
        time.sleep(10)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        time.sleep(2)
        self.click(self.REGIST_BUTTON)
        self.input_text(self.ORGANIZATION_TEXT, self.config_dict['subscription_organization'])
        self.input_text(self.KEY_TEXT, self.config_dict['subscription_key'])
        time.sleep(1)
        self.click(self.REGIST_COMMIT_BUTTON)
        time.sleep(60)
        self.refresh()
        time.sleep(10)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        self.assert_text_in_element("//*[@id='app']/div/div/label", "Status: Current")
        self.click(self.DETAIL_BUTTON)
        time.sleep(2)
        self.assert_text_in_element(self.DETALI_PRODUCT_NAME, "Red Hat Virtualization Host")
        self.assert_text_in_element(self.DETAIL_PRODUCT_ID,"328")
        self.assert_text_in_element(self.DETAIL_PRODUCT_VERSION, "4.3")
        self.assert_text_in_element(self.DETAIL_PRODUCT_STATUS, "Subscribed")

    def create_sos_report(self):
        self.host.execute("yes|sosreport", timeout=2000)
        ret = self.host.execute('ls /var/tmp/')
        for f in ret.split('\n'):
            file = f.rstrip()
            if file.startswith("sosreport-") and file.endswith(".tar.xz"):
                tar_file_path = os.path.join('/var/tmp', file)
                self.host.execute('tar -xvJf %s' % tar_file_path)
    
    def find_nodectl_info_file(self):
        ret = self.host.execute('ls')
        for file in ret.split(' '):
            if file.startswith("sosreport-"):
                nodectl_info_file = os.path.join('/root', file, 'sos_commands/ovirt_node/nodectl_info')
                return nodectl_info_file

    def check_nodectl_info_file(self, info_file):
        ret = self.host.execute("nodectl info")
        self.host.get_file(info_file, './nodectl_info')
        with open('./nodectl_info') as file:
            for line in file.readlines():
                result = re.search('fail', line)
                self.assertEqual(result, None)

        for line in ret.split('\n'):
            des_line = line.replace('\n','').replace('\r','')
            with open('./nodectl_info') as file:
                for line in file.readlines():
                    res_line = line.replace('\n','').replace('\r','')
                    if res_line == des_line:
                        break
                    else:
                        continue
            continue
        os.remove('./nodectl_info')
    
    def config_system_purpose(self):
        self.host.execute("syspurpose set-role 'Red Hat Enterprise Linux Compute Node'")
        self.host.execute("syspurpose set-sla 'Self-Support'")
        self.host.execute("syspurpose set-usage 'Test'")
        self.click(self.SUBSCRIPTION_LINK)
        time.sleep(5)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        time.sleep(10)

    def remove_libvirt(self):
        cmd = 'yum remove libvirt'
        output = self.host.execute(cmd).stdout
        result = re.search("Error",output)
        self.assertNotEqual(result, None)