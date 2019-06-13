import simplejson
import time
import yaml
from seleniumlib import SeleniumTest


class CommonDashboardPage(SeleniumTest):
    """
    :avocado: disable
    """

    COMMON_DASHBOARD_FRAME_NAME = "/dashboard"
    NAVBAR_DASHBOARD = "//ul[@id='main-navbar']/li[position()=3]"

    BTN_ADD_HOSTS = "//button[@id='dashboard-add']"

    #Add machine to dashboard dialog
    INPUT_ADD_HOST_ADDR = "//input[@id='add-machine-address']"
    BTN_ADD_IN_DIALOG = "//div[@id='dashboard_setup_server_dialog']/div/div/div[@class='modal-footer']/button[contains(text(),'Add')]"
    UNKNOWN_HOST_KEY = "//div[@id='dashboard_setup_server_dialog']/div/div/div[@class='modal-header']/h4[contains(text(),'Unknown Host Key')]"
    BTN_CONNECT_IN_DIALOG = "//div[@id='dashboard_setup_server_dialog']/div/div/div[@class='modal-footer']/button[contains(text(),'Connect')]"
    INPUT_PASSWORD_AUTHENTICATION = "//input[@id='login-custom-password']"
    BTN_LOGIN_IN_DIALOG = "//div[@id='dashboard_setup_server_dialog']/div/div/div[@class='modal-footer']/button[contains(text(),'Log In')]"

    #Servers
    LIST_DASHBOARD_HOSTS = "//div[@id='dashboard-hosts']"
    ITEM_LOCALHOST_DASHBOARD_HOSTS = "//div[@id='dashboard-hosts']/div[@class='list-group']/a[@data-address='{}']"

    def open_page(self):
        self.click(self.NAVBAR_DASHBOARD)
        self.switch_to_frame(self.COMMON_DASHBOARD_FRAME_NAME)
    
    def add_remote_hosts(self):
        self.click(self.BTN_ADD_HOSTS)
        config = self.get_data('common_dashboard.yml')
        config_dict = yaml.load(open(config))
        self.input_text(self.INPUT_ADD_HOST_ADDR, config_dict['remote_host'])
        time.sleep(1)
        self.click(self.BTN_ADD_IN_DIALOG)
        time.sleep(1)
        if self.UNKNOWN_HOST_KEY:  ####need to do more research
            self.click(self.BTN_CONNECT_IN_DIALOG)
            time.sleep(1)

        self.input_text(self.INPUT_PASSWORD_AUTHENTICATION, config_dict['password_root'])
        self.click(self.BTN_LOGIN_IN_DIALOG)
        time.sleep(5)

        #check result
        self.assert_element_visible(self.ITEM_LOCALHOST_DASHBOARD_HOSTS.format(config_dict['remote_host']))



    