import os
import yaml
import time
import datetime
import simplejson
import urllib2
import stat
import re
#import pytz
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
    R_MACHINE_ADDR="10.73.73.106"
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
    DASHBOARD_LINK = "//*[@id='main-navbar']/li[3]/a/span[1]"
    OVIRT_HOSTEDENGINE_FRAME_NAME = "/ovirt-dashboard"

    #add and delete remote host
    INPUT_REMOTE_USER="//*[@id='login-custom-user']"
    INPUT_REMOTE_PASSWORD="//*[@id='login-custom-password']"
    SET_UP_SERVER="//*[@id='dashboard_setup_server_dialog']/div/div/div[3]/button[2]"
    ADD_SERVER_BUTTON="//*[@id='dashboard-add']"
    INPUT_MACHINE_ADDRESS="//*[@id='add-machine-address']"
    ADD_BUTTON="//*[@id='dashboard_setup_server_dialog']/div/div/div[3]/button[2]"
    ADD_UNKNOWN_HOST="//*[@id='add-unknown-host']"
    CONNECT_BUTTON="//*[@id='dashboard_setup_server_dialog']/div/div/div[3]/button[2]"

    EDITE_SERVER="//*[@id='dashboard-enable-edit']"
    DELETE_SERVER="//*[@id='dashboard-hosts']/div[2]/a[1]/button[1]"

    #subscription
    NETWORK_INFO_LINK="//*[@id='content']/div/div/div[1]/table/tbody[4]/tr[1]/td[2]/a"
    SUBSCRIPTION_LINK="//*[@id='sidebar-tools']/li[4]/a"
    SUBSCRIPTION_FRAME_NAME="/subscriptions"
    REGIST_BUTTON="//*[@id='app']/div/div/button"
    CHOOSE_URL_BUTTON="//*[@id='subscription-register-url']/button"
    CUSTOM_URL_BUTTON="//*[@id='subscription-register-url']/ul/li[2]/a"
    CUSTOM_URL_TEXT="//*[@id='subscription-register-url-custom']"
    SUBSCRIPTION_USER_TEXT="//*[@id='subscription-register-username']"
    SUBSCRIPTION_PWD_TEXT="//*[@id='subscription-register-password']"
    REGIST_COMMIT_BUTTON="//*[@id='cockpit_modal_dialog']/div/div[2]/div/div/div[3]/button[2]"
    DETAIL_BUTTON = "//*[@id='app']/div/table/tbody/tr[1]/td/i"
    DETALI_PRODUCT_NAME = "//*[@id='app']/div/table/tbody/tr[2]/td/div[2]/table/tbody/tr[1]/td[2]/span"
    DETAIL_PRODUCT_ID = "//*[@id='app']/div/table/tbody/tr[2]/td/div[2]/table/tbody/tr[2]/td[2]/span"
    DETAIL_PRODUCT_VERSION = "//*[@id='app']/div/table/tbody/tr[2]/td/div[2]/table/tbody/tr[3]/td[2]/span"
    DETAIL_PRODUCT_STATUS = "//*[@id='app']/div/table/tbody/tr[2]/td/div[2]/table/tbody/tr[5]/td[2]/span"
    ORGANIZATION_TEXT= "//*[@id='subscription-register-org']"
    KEY_TEXT="//*[@id='subscription-register-key']"

    #add nfs
    STORAGE_LINK="//*[@id='sidebar-menu']/li[3]/a/span"
    STORAGE_FRAME_NAME="/storage"
    ADD_NFS_BUTTON="//*[@id='nfs-mounts']/div[1]/div/button"
    NFS_SERVER_ADDR_TEXT="//*[@id='dialog']/div/div[2]/form/div[1]/input"
    SERVER_PATH_TEXT="//*[@id='dialog']/div/div[2]/form/div[2]/div/div/div/input"
    MOUNT_POINT_TEXT="//*[@id='dialog']/div/div[2]/form/div[3]/input"
    NFS_ADD_BUTTON="//*[@id='dialog']/div/div[3]/button[2]"

    NFS_SERVER_DETAIL_BUTTON="//*[@id='nfs-mounts']/table/tbody/tr/td[1]"
    DELETE_NFS_SERVER_BUTTON="//*[@id='detail-header']/div/div[1]/span/button[3]"
    NFS_UNMOUNT_BUTTON="//*[@id='detail-header']/div/div[1]/span/button[1]"
    NFS_SIZE_FIELD="//*[@id='detail-header']/div/div[2]/div/div[3]"
    NFS_SIZE_PROGRESS="//*[@id='detail-header']/div/div[2]/div/div[3]/div"

    #system status
    CPU_STATUS="//*[@id='dashboard-plot-0']"
    MEMORY_LINK="//*[@id='dashboard']/div[1]/div/ul/li[2]/a"
    MEMORY_STATUS="//*[@id='dashboard-plot-1']"
    NETWORK_LINK="//*[@id='dashboard']/div[1]/div/ul/li[3]/a"
    NETWORK_STATUS="//*[@id='dashboard-plot-2']"
    DISK_LINK="//*[@id='dashboard']/div[1]/div/ul/li[4]/a"
    DISK_STATUS="//*[@id='dashboard-plot-3']"

    #config hostname
    SYSTEM_FRAME_LINK="//*[@id='sidebar-menu']/li[1]/a"
    SYSTEM_FRAME_NAME="/system"
    HOSTNAME_BUTTON="//*[@id='system_information_hostname_button']"
    PRETTY_HOSTNAME_TEXT="//*[@id='sich-pretty-hostname']"
    REAL_HOSTNAME_TEXT="//*[@id='sich-hostname']"
    HOSTNAME_APPLY_BUTTON="//*[@id='sich-apply-button']"

    #config timezone
    TIME_LINK="//*[@id='system_information_systime_button']"
    # TIMEZONE_TEXT="//*[@id='systime-timezonesundefined']"
    TIMEZONE_REMOVER="//*[@id='systime-timezonesundefined']//parent::*/span"
    TIMEZONE_DROPDOWN="//*[@id='systime-timezonesundefined']//parent::*/span"
    TIMEZONE_ITEM="//*[@id='systime-timezonesundefined']//parent::*/ul/li[1]"
    TIMEZONE_APPLY_BUTTON="//*[@id='systime-apply-button']"
    TIME_SET_DROPDOWN="//*[@id='change_systime']/button"
    TIME_SET_MANUALLY="//*[@id='change_systime']/ul/li[1]/a"
    TIME_MIN_TEXT="//*[@id='systime-time-minutes']"

    #restart node
    RESTART_BUTTON="//*[@id='shutdown-group']/button[1]"
    LEAVE_MESSAGE_TEXT="//*[@id='shutdown-dialog']/div/div/div[2]/textarea"
    RESTART_APPLY_BUTTON="//*[@id='shutdown-dialog']/div/div/div[3]/button[2]"
    RECONNECT_BUTTON="//*[@id='machine-reconnect']"

    #change the performance profile
    PROFILE_LINK="//*[@id='tuned-status-tooltip']/a"
    DESKTOP_OPTION="//*[@id='cockpit_modal_dialog']/div/div[2]/div/div/div[2]/div/div[3]"
    PROFILE_APPLY_BUTTON="//*[@id='cockpit_modal_dialog']/div/div[2]/div/div/div[3]/button[2]"

    #kernel dump
    KD_LINK="//*[@id='sidebar-tools']/li[2]/a"
    #//*[@id="sidebar-tools"]/li[3]/a //*[@id="sidebar-tools"]/li[2]/a //*[@id="sidebar-tools"]/li[3]
    HINT="//*[@id='app']/div/form/div[2]/a/span"
    KDUMP_SERVICE_STATUS="//*[@id='app']/div/form/div[1]/a/span"
    BTN_TEST_CONFIGURATION="//*[@id='app']/div/form/div[2]/button"
    CRASH_SYSTEM_BUTTON="//*[@id='cockpit_modal_dialog']/div/div[2]/div/div/div[3]/button[2]"

    KD_FRAME_NAME="/kdump"
    KD_SERVICE_LINK="//*[@id='app']/div/form/div[1]/a/span"
    SERVICES_LINK="//*[@id='sidebar-menu']/li[7]/a/span"
    SERVICE_FRAME_NAME="/system/services"
    SERVICE_SEARCHER="//*[@id='services-text-filter']"
    KD_SERVICE_LINK="//*[@id='services-list']/div/table/tbody/tr/td[1]"
    STOP_START_BUTTON="//*[@id='service-unit-primary-action']/button"
    KD_STATUS_INFO="//*[@id='service-unit']/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/span"
    KD_RESTART_BUTTON="//*[@id='service-unit-action']/button[1]"
    KD_DISABLE_BUTTON="//*[@id='service-file-action']/button[1]"
    KD_ENABLE_TEXT="//*[@id='service-unit']/div/div[2]/div[1]/table/tbody/tr[3]/td[2]"

    #check system logs
    # LOGS_LINK="//*[@id='content']/div/div/div[1]/table/tbody[4]/tr[2]/td[2]/a"
    LOGS_LINK="//*[@id='sidebar-menu']/li[2]/a/span"
    LOGS_FRAME_NAME="/system/logs"
    LOGS_DURATION_BUTTON="//*[@id='journal-current-day-menu']/button"
    RECENT_LOGS="//*[@id='journal-current-day-menu']/ul/li[1]/a"
    # CURRENT_BOOT="//*[@id='journal-current-day-menu']/ul/li[2]/a"
    # LAST_ONE_DAY="//*[@id='journal-current-day-menu']/ul/li[4]/a"
    LAST_SEVEN_DAYS="//*[@id='journal-current-day-menu']/ul/li[5]/a"
    LOGS_LOAD_EARLIER="//*[@id='journal-load-earlier']"
    LOGS_FILTER="//*[@id='journal-prio-menu']/button"
    LOGS_EVERYTHING="//*[@id='prio-lists']/li[1]/a"
    LOGS_WARNING_ICON="//*[@id='journal-box']/div[1]/div[2]/div[1]"

    #create new account
    ACCOUNT_LINK="//*[@id='sidebar-menu']/li[6]/a"
    ACCOUNT_FRAME_NAME="/users"
    CREATE_NEW_ACCOUNT_BUTTON="//*[@id='accounts-create']"
    FULL_NAME_TEXT="//*[@id='accounts-create-real-name']"
    PASSWORD_TEXT="//*[@id='accounts-create-pw1']"
    CONFIRM_TEXT="//*[@id='accounts-create-pw2']"
    CREATE_BUTTON="//*[@id='accounts-create-create']"
    ACCOUNT_INFO="//*[@id='accounts-list']/div/div[3]"

    ROOT_BUTTON="//*[@id='navbar-dropdown']"
    LOGOUT_BUTTON="//*[@id='go-logout']"
    LOGIN_USERNAME_TEXT="//*[@id='login-user-input']"
    LOGIN_PWD_TEXT="//*[@id='login-password-input']"
    LOGIN_BUTTON="//*[@id='login-button']"

    #terminal function
    TERMINAL_LINK="//*[@id='sidebar-tools']/li[5]/a"
    TERMINAL_FRAME_NAME="/system/terminal"
    TERMINAL_ADMIN="//*[@id='terminal']/div/div[2]/div/div/div[1]/div[1]/div[5]"
    CONMMAND_LINE="//*[@id='terminal']/div/div[2]/div/div/div[1]/div[1]/div[7]"

    SSH_HOST_KEY_LINK="//*[@id='content']/div/div/div[1]/table/tbody[5]/tr/td[2]/a"
    SSH_HOST_KEY_COTENT="//*[@id='content']/div/div/div[1]/table/tbody[5]/tr/td[2]/div/div/div/div/div[2]/div"

    #check diagnostic report
    DIAGNOSTIC_REPORT_LINK="//*[@id='sidebar-tools']/li[1]/a"
    DIAGNOSTIC_REPORT_FRAME="/sosreport"
    CREATE_REPORT_BUTTON="//button[text()='Create Report']"
    REPORT_DIALOG="//*[@id='sos']/div"
    REPORT_DOWNLOAD_BUTTON="//*[@id='sos-download']/center/button"
    
    #check_selinux_policy
    SELINUX_LINK="//*[@id='sidebar-tools']/li[3]/a"
    SELINUX_FRAME="/selinux/setroubleshoot"
    SWITCH_BUTTON="//*[@id='app']/div/div/label/label/span"

    #check udisks
    SERVICE_LINK="//*[@id='sidebar-menu']/li[7]/a"
    FILTER_INPUT_TEXT="//*[@id='services-text-filter']"
    UDISKS_STATUS_TEXT="//*[@id='services-list']/div/table/tbody/tr/td[2]"



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
        cmd = 'systemctl status cockpit'
        output = host.execute(cmd).stdout
        result = re.search('active', output)
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
        expect_s = self.R_MACHINE_ADDR + '/ovirt-dashboard'
        self.assertEqual(actual_s,expect_s)

    def login_wrong_remote_machine(self):
        time.sleep(2)
        self.click(self.OTHER_OPTION)
        self.input_text(self.SERVER_FIELD,self.WRONG_ADDR)
        self.login(self.R_MACHINE_USER,self.R_MACHINE_PWD)
        time.sleep(15)
        self.assertEqual(self.get_text(self.LOGIN_ERROR_MESSAGE),"Unable to connect to that address")

        
    def add_remote_host(self):
        self.click(self.DASHBOARD_LINK)
        time.sleep(1)
        self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)

        self.click(self.ADD_SERVER_BUTTON)
        time.sleep(5)
        self.input_text(self.INPUT_MACHINE_ADDRESS,self.R_MACHINE_ADDR)
        time.sleep(5)
        self.click(self.ADD_BUTTON)
        time.sleep(5)
        self.click(self.CONNECT_BUTTON)
        time.sleep(5)
        self.input_text(self.INPUT_REMOTE_USER,self.R_MACHINE_USER)
        self.input_text(self.INPUT_REMOTE_PASSWORD,self.R_MACHINE_PWD)
        self.click(self.SET_UP_SERVER)
        self.assert_element_visible("//*[@id='dashboard-hosts']/div[2]/a[2]")

    def delete_remote_host(self):
        self.click(self.DASHBOARD_LINK)
        time.sleep(1)
        self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)

        self.click(self.EDITE_SERVER)
        time.sleep(2)
        self.click(self.DELETE_SERVER)
        time.sleep(2)
        self.assert_element_invisible("//*[@id='dashboard-hosts']/div[2]/a[2]")
    
    def subscription_to_rhsm(self):
        self.host.execute("subscription-manager config --server.hostname=subscription.rhsm.stage.redhat.com")
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SUBSCRIPTION_LINK)
        time.sleep(10)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        time.sleep(2)
        self.click(self.REGIST_BUTTON)
        self.input_text(self.SUBSCRIPTION_USER_TEXT, self.config_dict['subscription_username'])
        self.input_text(self.SUBSCRIPTION_PWD_TEXT, self.config_dict['subscription_password'])
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

    def check_packages_installation(self):
        self.host.execute("subscription-manager config --rhsm.baseurl=https://cdn.stage.redhat.com")
        self.host.execute("subscription-manager repos --disable=*")
        self.host.execute("subscription-manager repos --enable=%s" %self.config_dict['subscription_repos'])
        sub_pkgs = self.config_dict['subscription_packages']
        for pkg in sub_pkgs[:-1]:
            ret = self.host.execute("yum install -y %s" % pkg, timeout=200)
            self.assertTrue('Complete!' in ret.stdout)
        self.assertTrue('rhvm-appliance' in self.host.execute("yum search %s" %sub_pkgs[-1]))


    def add_nfs_storage(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.STORAGE_LINK)
        self.switch_to_frame(self.STORAGE_FRAME_NAME)
        time.sleep(2)
        self.click(self.ADD_NFS_BUTTON)
        time.sleep(2)
        self.input_text(self.NFS_SERVER_ADDR_TEXT, self.config_dict['nfs_ip'])
        time.sleep(1)
        self.input_text(self.SERVER_PATH_TEXT, self.config_dict['nfs_dir'])
        time.sleep(1)
        self.input_text(self.MOUNT_POINT_TEXT, self.config_dict['nfs_mount_point'])
        time.sleep(1)
        nfs_text = self.config_dict['nfs_ip'] + " " + self.config_dict['nfs_dir']
        self.click(self.NFS_ADD_BUTTON)
        time.sleep(3)
        self.assert_text_in_element(self.NFS_SERVER_DETAIL_BUTTON, nfs_text)
        self.click(self.NFS_SERVER_DETAIL_BUTTON)
        time.sleep(3)
        self.click(self.DELETE_NFS_SERVER_BUTTON)
        time.sleep(2)
        self.assert_text_not_in_element(self.NFS_SERVER_DETAIL_BUTTON, nfs_text)
    
    def system__dynamic_status(self):
        self.click(self.DASHBOARD_LINK)
        time.sleep(1)
        self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)
        time.sleep(3)
        self.assert_element_visible(self.CPU_STATUS)

        self.click(self.MEMORY_LINK)
        time.sleep(3)
        self.assert_element_visible(self.MEMORY_STATUS)
        
        self.click(self.NETWORK_LINK)
        time.sleep(3)
        self.assert_element_visible(self.NETWORK_STATUS)

        self.click(self.DISK_LINK)
        time.sleep(3)
        self.assert_element_visible(self.DISK_STATUS)
    
    def config_hostname(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SYSTEM_FRAME_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        self.click(self.HOSTNAME_BUTTON)

        self.input_text(self.PRETTY_HOSTNAME_TEXT,"test")
        time.sleep(1)
        self.input_text(self.REAL_HOSTNAME_TEXT,"test.redhat.com")
        time.sleep(1)
        self.click(self.HOSTNAME_APPLY_BUTTON)
        time.sleep(2)

        self.assert_text_in_element(self.HOSTNAME_BUTTON,"test (test.redhat.com)")

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
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SYSTEM_FRAME_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)

        self.click(self.TIME_LINK)
        self.click(self.TIME_SET_DROPDOWN)
        self.click(self.TIME_SET_MANUALLY)
        self.input_text(self.TIME_MIN_TEXT,"00")
        self.click(self.TIMEZONE_APPLY_BUTTON)
        time.sleep(2)
        self.refresh()
        time.sleep(5)
        self.switch_to_frame(self.SYSTEM_FRAME_NAME)
        actual_now = self.get_text(self.TIME_LINK).split(':')[-1]
        self.assertEqual(actual_now,"00")
    
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
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SYSTEM_FRAME_LINK)
        time.sleep(1)
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
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SERVICES_LINK)
        self.switch_to_frame(self.SERVICE_FRAME_NAME)
        self.input_text(self.SERVICE_SEARCHER, 'kdump')
        time.sleep(2)
        self.click(self.KD_SERVICE_LINK)
        time.sleep(2)
        self.click(self.STOP_START_BUTTON)
        time.sleep(8)
        self.assert_text_in_element(self.KD_STATUS_INFO,"inactive")
        self.click(self.STOP_START_BUTTON)
        self.assert_text_in_element(self.KD_STATUS_INFO,"activating")
        self.click(self.KD_RESTART_BUTTON)
        time.sleep(8)
        self.assert_text_in_element(self.KD_STATUS_INFO,"active")
        self.click(self.KD_DISABLE_BUTTON)
        time.sleep(8)
        self.assert_text_in_element(self.KD_ENABLE_TEXT,"disabled")
        self.click(self.KD_DISABLE_BUTTON)
        time.sleep(8)
        self.assert_text_in_element(self.KD_ENABLE_TEXT,"enabled")
    
    def check_file_system_list(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.STORAGE_LINK)
        time.sleep(5)
        self.switch_to_frame(self.STORAGE_FRAME_NAME)
        
        self.assert_text_in_element("//*[@id='storage_mounts']/tr[8]/td[2]/div","/boot")
        self.click("//*[@id='storage_mounts']/tr[1]/td[2]/div")
        time.sleep(1)
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[2]/tr[1]/td[2]/span","1 GiB")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[5]/tr[1]/th","root")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[6]/tr[1]/td[2]/span","1 GiB")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[6]/tr[1]/th","/tmp")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[7]/tr[1]/td[2]/span","15 GiB")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[7]/tr[1]/th","/var")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[8]/tr[1]/td[2]/span","10 GiB")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[8]/tr[1]/th","/var_crash")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[9]/tr[1]/td[2]/span","8 GiB")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[9]/tr[1]/th","/var_log")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[10]/tr[1]/td[2]/span","2 GiB")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[10]/tr[1]/th","/var_log_audit")
        self.assert_text_in_element("//*[@id='detail-content']/table/tbody[11]/tr[1]/th","swap")
    
    def modify_nfs_storage(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
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
        self.assert_element_visible(self.NFS_SIZE_PROGRESS)
        self.click(self.DELETE_NFS_SERVER_BUTTON)
        time.sleep(2)
        self.assert_element_invisible("//*[@id='nfs-mounts']/table/tbody/tr")
    
    def check_the_logs(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.LOGS_LINK)
        self.switch_to_frame(self.LOGS_FRAME_NAME)

        self.click(self.LOGS_DURATION_BUTTON)
        time.sleep(1)
        self.click(self.RECENT_LOGS)
        time.sleep(3)
        self.assert_element_invisible(self.LOGS_LOAD_EARLIER)
        self.assert_element_visible(self.LOGS_WARNING_ICON)
        self.click(self.LOGS_DURATION_BUTTON)
        time.sleep(1)
        self.click(self.LAST_SEVEN_DAYS)
        time.sleep(3)
        self.assert_element_visible(self.LOGS_LOAD_EARLIER)
        self.click(self.LOGS_FILTER)
        time.sleep(2)
        self.click(self.LOGS_EVERYTHING)
        time.sleep(3)
        try:
            self.assert_element_visible(self.LOGS_WARNING_ICON)
        except:
            pass

    def create_new_account(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.ACCOUNT_LINK)
        time.sleep(1)
        self.switch_to_frame(self.ACCOUNT_FRAME_NAME)

        self.click(self.CREATE_NEW_ACCOUNT_BUTTON)
        time.sleep(3)
        self.input_text(self.FULL_NAME_TEXT,"user_a")
        self.input_text(self.PASSWORD_TEXT,"shleishlei123")
        self.input_text(self.CONFIRM_TEXT,"shleishlei123")
        self.click(self.CREATE_BUTTON)
        time.sleep(2)
        self.assert_element_visible(self.ACCOUNT_INFO)

        self.switch_to_default_content()
        self.click(self.ROOT_BUTTON)
        self.click(self.LOGOUT_BUTTON)
        time.sleep(1)
        self.input_text(self.LOGIN_USERNAME_TEXT,"user_a")
        self.input_text(self.LOGIN_PWD_TEXT,"shleishlei123")
        self.click(self.LOGIN_BUTTON)
        time.sleep(3)
        self.assert_frame_available("/users")
    

    def check_terminal(self):
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.TERMINAL_LINK)
        time.sleep(1)
        self.switch_to_frame(self.TERMINAL_FRAME_NAME)
        time.sleep(3)
        self.click(self.CONMMAND_LINE)
        self.input_text(self.CONMMAND_LINE," nodectl check\r\n",False)
        time.sleep(5)
        self.assert_text_in_element("//*[@id='terminal']/div/div[2]/div/div/div[1]/div[1]/div[8]","Status")

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
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
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
        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
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

        self.click(self.LOCALHOST_LINK)
        time.sleep(1)
        self.click(self.SERVICE_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SERVICE_FRAME_NAME)
        self.input_text(self.FILTER_INPUT_TEXT,"udisks")
        time.sleep(3)
        self.assert_text_in_element(self.UDISKS_STATUS_TEXT,"active (running)")

        cmd = 'systemctl status udisks2'
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
        time.sleep(5)
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
        time.sleep(5)
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
