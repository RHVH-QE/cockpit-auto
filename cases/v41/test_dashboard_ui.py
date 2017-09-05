from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.dashboard_nodestatus_page import NodeStatusPage
from fabric.api import env, run, settings
from cases import CONF
import const
import logging
from utils.helpers import checkpoint

log = logging.getLogger("sherry")

dict1 = dict(zip(const.dashboard_ui, const.dashboard_ui_id))

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
    log.info("Test dashboard_ui-->Trying to login to cockpit...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


@checkpoint(dict1)
def check_node_status_func(ctx):
    """
    RHEVM-18534
        Check node status in virtualization dashboard.
    """
    log.info("Checking node status in virtualization dashboard...")
    node_status_page = NodeStatusPage(ctx)
    node_status_page.check_node_status()


@checkpoint(dict1)
def check_node_health_func(ctx):
    """
    RHEVM-18535
        Check node health in virtualization dashboard
    """
    log.info("Checking node health in virtualization dashboard...")
    node_status_page = NodeStatusPage(ctx)
    node_status_page.check_node_health(is_registerd=True)


@checkpoint(dict1)
def check_node_info_func(ctx):
    """
    RHEVM-18536
        Check node health in virtualization dashboard
    """
    log.info("Checking node info in virtualization dashboard... ")
    node_status_page = NodeStatusPage(ctx)
    test_layer = test_build + '+1'
    print test_layer
    node_status_page.check_node_info(test_layer)


@checkpoint(dict1)
def check_network_func(ctx):
    """
    RHEVM-18540
        Go to the Networking page in virtualization dashboard
    """

    log.info("Checking networking page in virtualization dashboard...")
    node_status_page = NodeStatusPage(ctx)
    node_status_page.check_network()


@checkpoint(dict1)
def check_system_log_func(ctx):
    """
    RHEVM-18541
        Go to the Logs page in virtualization dashboard
    """
    log.info("Checking logs page in virtualization dashboard...")
    node_status_page = NodeStatusPage(ctx)
    node_status_page.check_system_log()


@checkpoint(dict1)
def check_storage_func(ctx):
    """
    RHEVM-18542
        Go to the Storage page in virtualization dashboard
    """
    log.info("Checking storage page in virtualization dashboard...")
    node_status_page = NodeStatusPage(ctx)
    node_status_page.check_storage()


@checkpoint(dict1)
def check_ssh_key_func(ctx):
    """
    RHEVM-18543
        Check the ssh host key in virtualization dashboard
    """
    log.info("Checking ssh host key in virtualization dashboard...")
    node_status_page = NodeStatusPage(ctx)
    node_status_page.check_ssh_key()


def runtest():
    ctx = init_browser()
    test_login(ctx)
    import sys
    from utils.helpers import call_func_by_name
    for ckp in dict1.keys():
        call_func_by_name(sys.modules[__name__], ckp, ctx)
    ctx.close()
