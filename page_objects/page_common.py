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

    LOGIN_ERROR_MESSAGE="//*[@id='login-error-message']"

    OTHER_OPTION="//*[@id='show-other-login-options']"
    SERVER_FIELD="//*[@id='server-field']"

    SLEEP_TIME = 5
    OVIRT_DASHBOARD_FRAME_NAME = "/dashboard"
    DASHBOARD_LINK = "//*[@id='main-navbar']/li[3]/a/span[1]"
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
        #self.click(self.CONNECT_BUTTON)
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