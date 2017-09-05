from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.dashboard_nodestatus_page import NodeStatusPage
from fabric.api import env, run, settings
from cases import CONF
from collections import OrderedDict
from utils.helpers import checkpoint
import const
import logging


log = logging.getLogger("sherry")

dict1 = OrderedDict(zip(const.dashboard_ui_efi, const.dashboard_ui_efi_id))

host_ip, host_user, host_password, test_build, rhvm_fqdn, browser = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('common').get(
            'test_build'), CONF.get('common').get('rhvm_fqdn'), CONF.get('common').get('browser')

env.host_string = host_user + '@' + host_ip
env.password = host_password


def init_browser():
    if browser == 'firefox':
        driver = webdriver.Firefox()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
    elif browser == 'chrome':
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
    else:
        raise NotImplementedError


def test_login(ctx):
    log.info("Test dashboard_ui_efi-->Trying to login to cockpit...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


# This will be tested on a rhvh with EFI
@checkpoint(dict1)
def check_nodestatus_efi(ctx):
    """
    RHEVM-18539
        Check node status with EFI
    """
    log.info("Checking node status with EFI... ")
    node_status_page = NodeStatusPage(ctx)
    test_layer = test_build + '+1'
    node_status_page.check_node_status_efi(test_layer)


def runtest():
    ctx = init_browser()
    test_login(ctx)
    import sys
    from utils.helpers import call_func_by_name
    for ckp in dict1.keys():
        call_func_by_name(sys.modules[__name__], ckp, ctx)
    ctx.close()
