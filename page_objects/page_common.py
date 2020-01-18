import os
import yaml
import time
import datetime
import simplejson
import urllib2
import stat
import re
from seleniumlib import SeleniumTest
from utils.htmlparser import MyHTMLParser
from utils.machine import Machine
from utils.rhvmapi import RhevmAction
from selenium import webdriver



class CommonPages(SeleniumTest):
    """
    :avocado: disable
    """

    R_MACHINE_ADDR="10.66.9.205"
    R_MACHINE_USER="root"
    R_MACHINE_PWD="redhat"

    RHSM_CUSTOM_URL="subscription.rhsm.stage.redhat.com"
    RHSM_USER="shlei2"
    RHSM_PWD="lsystc571998"

    NFS_SERVER_ADDR="10.66.10.132"
    SERVER_PATH="/home/shiyilei/nfs"
    MOUNT_POINT="/root/mnt"

    LOGIN_ERROR_MESSAGE="//*[@id='login-error-message']"

    OTHER_OPTION="//*[@id='show-other-login-options']"
    SERVER_FIELD="//*[@id='server-field']"

    SLEEP_TIME = 5
    OVIRT_DASHBOARD_FRAME_NAME = "/dashboard"
    DASHBOARD_LINK = "//*[@id='main-navbar']/li[3]/a/span[1]"
    OVIRT_HOSTEDENGINE_FRAME_NAME = "/ovirt-dashboard"
    # DASHBOARD_FRAME_NAME="cockpit1:localhost/dashboard"
    # SYSTEM_FRAME_NAME="cockpit1:localhost/system"

    #add and delete remote host
    INPUT_REMOTE_USER="//*[@id='login-custom-user']"
    INPUT_REMOTE_PASSWORD="//*[@id='login-custom-password']"
    SET_UP_SERVER="//*[@id='dashboard_setup_server_dialog']/div/div/div[3]/button[2]"

    ADD_SERVER_BUTTON="//*[@id='dashboard-add']"
    INPUT_MACHINE_ADDRESS="//*[@id='add-machine-address']"
    ADD_BUTTON="//*[@id='dashboard_setup_server_dialog']/div/div/div[3]/button[2]"
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

    #add nfs
    STORAGE_LINK="//*[@id='content']/div/div/div[1]/table/tbody[4]/tr[3]/td[2]/a"
    STORAGE_FRAME_NAME="/storage"
    ADD_NFS_BUTTON="//*[@id='nfs-mounts']/div[1]/div/button"
    NFS_SERVER_ADDR_TEXT="//*[@id='dialog']/div/div[2]/form/div[1]/input"
    SERVER_PATH_TEXT="//*[@id='dialog']/div/div[2]/form/div[2]/div/div/div/input"
    MOUNT_POINT_TEXT="//*[@id='dialog']/div/div[2]/form/div[3]/input"
    NFS_ADD_BUTTON="//*[@id='dialog']/div/div[3]/button[2]"

    NFS_SERVER_DETAIL_BUTTON="//*[@id='nfs-mounts']/table/tbody/tr/td[1]"
    DELETE_NFS_SERVER_BUTTON="//*[@id='detail-header']/div/div[1]/span/button[3]"


    def setUp(self):
        case_name = self._testMethodName
        # config = self.get_data('cockpit_common.yml')
        # self.config_dict = yaml.load(open(config))
        
        if 'firefox' in case_name.split('_'):
            os.environ['BROWSER']='firefox'
        if 'chrome' in case_name.split('_'):
            os.environ['BROWSER']='chrome'
        if 'login' in case_name.split('_'):
            os.environ['USERNAME']='invalid_user'
            os.environ['PASSWD']='invalid_pwd'
        super(CommonPages, self).setUp()

    def open_page(self):

        # self.click(self.DASHBOARD_LINK)

        # time.sleep(1)
        # self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)
        pass
    
    def check_firefox_login(self):
        self.assertEqual(self.get_text(self.LOGIN_ERROR_MESSAGE),"Wrong user name or password")

        config_dict = yaml.load(open('./config.yml'))
        os.environ['USERNAME'] = config_dict['host_user']
        os.environ['PASSWD'] = config_dict['host_pass']

        host_string = os.environ.get('HOST_STRING')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')

        host = Machine(host_string, username, passwd)

        self.login(username, passwd)
        # self.open_page()

        cmd = 'systemctl status cockpit'
        output = host.execute(cmd).stdout
        result = re.search('active (running)', output)
        self.assertNotEqual(result, 'None')
        
    def check_chrome_login(self):
        self.check_firefox_login()

    def login_remote_machine(self):
        time.sleep(2)
        self.click(self.OTHER_OPTION)
        self.input_text(self.SERVER_FIELD,self.R_MACHINE_ADDR)
        self.login(self.R_MACHINE_USER,self.R_MACHINE_PWD)
        time.sleep(2)
        self.assert_frame_available("/ovirt-dashboard")
        
    def add_remote_host(self):

        self.click(self.DASHBOARD_LINK)
        time.sleep(1)
        self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)

        self.click(self.ADD_SERVER_BUTTON)
        self.input_text(self.INPUT_MACHINE_ADDRESS,self.R_MACHINE_ADDR)
        self.click(self.ADD_BUTTON)
        self.click(self.CONNECT_BUTTON)
        self.input_text(self.INPUT_REMOTE_USER,self.R_MACHINE_USER)
        self.input_text(self.INPUT_REMOTE_PASSWORD,self.R_MACHINE_PWD)
        self.click(self.SET_UP_SERVER)
        self.assert_element_visible("//*[@id='dashboard-hosts']/div[2]/a[2]")

    

    def delete_remote_host(self):
        self.click(self.DASHBOARD_LINK)
        time.sleep(1)
        self.switch_to_frame(self.OVIRT_DASHBOARD_FRAME_NAME)

        self.click(self.EDITE_SERVER)
        self.click(self.DELETE_SERVER)
    
    def subscription_to_rhsm(self):
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.click(self.NETWORK_INFO_LINK)
        self.switch_to_default_content()
        time.sleep(1)
        self.click(self.SUBSCRIPTION_LINK)
        time.sleep(1)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        self.click(self.REGIST_BUTTON)

        self.click(self.CHOOSE_URL_BUTTON)
        self.click(self.CUSTOM_URL_BUTTON)
        time.sleep(1)
        self.input_text(self.CUSTOM_URL_TEXT,self.RHSM_CUSTOM_URL)
        self.input_text(self.SUBSCRIPTION_USER_TEXT,self.RHSM_USER)
        self.input_text(self.SUBSCRIPTION_PWD_TEXT,self.RHSM_PWD)
        time.sleep(1)
        self.click(self.REGIST_COMMIT_BUTTON)
        time.sleep(20)
        self.refresh()
        time.sleep(10)
        self.switch_to_frame(self.SUBSCRIPTION_FRAME_NAME)
        self.click("//*[@id='app']/div/table/tbody/tr[1]/th")
        self.assert_text_in_element("//*[@id='app']/div/div/label","Status: Current")

        time.sleep(5)

    def add_nfs_storage(self):
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.click(self.STORAGE_LINK)
        self.switch_to_default_content()
        time.sleep(1)
        self.switch_to_frame(self.STORAGE_FRAME_NAME)
        self.click(self.ADD_NFS_BUTTON)

        self.input_text(self.NFS_SERVER_ADDR_TEXT,self.NFS_SERVER_ADDR)
        self.input_text(self.SERVER_PATH_TEXT,self.SERVER_PATH)
        self.input_text(self.MOUNT_POINT_TEXT,self.MOUNT_POINT)
        self.click(self.NFS_ADD_BUTTON)
        time.sleep(5)
        #self.assert_element_visible("//*[@id='nfs-mounts']/table/tbody/tr/td[1]")
        self.click(self.NFS_SERVER_DETAIL_BUTTON)
        time.sleep(3)
        self.assert_element_invisible(self.NFS_SERVER_DETAIL_BUTTON)
        