from selenium import webdriver
from fabric.api import env, run, settings
from pages.v41.nodectl import Nodectl
from cases import CONF
from collections import OrderedDict
from utils.helpers import checkpoint
import logging
import const


log = logging.getLogger("sherry")

dict1 = OrderedDict(zip(const.dashboard_nodectl, const.dashboard_nodectl_id))

host_ip, host_user, host_password, test_build, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('test_build'), CONF.get('common').get('browser')

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


@checkpoint(dict1)
def check_nodectl_help_func():
    """
    Purpose:
        RHEVM-18545
        Show nodectl help message in Terminal
    """
    log.info("Test dashboard_nodectl-->Checking nodectl help...")
    nodectl = Nodectl()
    nodectl.check_nodectl_help()


@checkpoint(dict1)
def check_nodectl_info_func():
    """
    Purpose:
        RHEVM-18547
        Show information about the image in Terminal
    """
    log.info("Checking nodectl info...")
    nodectl = Nodectl()
    nodectl.check_nodectl_info(test_build)


@checkpoint(dict1)
def check_nodectl_check_func():
    """
    Purpose:
        RHEVM-18550
        Check the system status in Terminal
    """
    log.info("Checking nodectl check...")
    nodectl = Nodectl()
    nodectl.check_nodectl_check()


@checkpoint(dict1)
def check_nodectl_debug_func():
    """
    Purpose:
        RHEVM-18551
        Check the debug information of nodectl sub_commands in Terminal
    """
    log.info("Checking nodectl debug...")
    nodectl = Nodectl()
    nodectl.check_nodectl_debug()


@checkpoint(dict1)
def check_nodectl_json_func():
    """
    Purpose:
        RHEVM-18552
        Check the JSON output for nodectl in Terminal
    """
    log.info("Checking nodectl json...")
    nodectl = Nodectl()
    nodectl.check_nodectl_json()


@checkpoint(dict1)
def check_nodectl_motd_func():
    """
    Purpose:
        RHEVM-18830
        Check the motd for nodectl in Terminal
    """
    log.info("Checking nodectl motd...")
    nodectl = Nodectl()
    nodectl.check_nodectl_motd()


@checkpoint(dict1)
def check_nodectl_banner_func():
    """
    Purpose:
        RHEVM-18831
        Check the generate-banner output for nodectl in Terminal
    """
    log.info("Checking nodectl banner...")
    nodectl = Nodectl()
    nodectl.check_nodectl_banner()


def runtest():
    import sys
    from utils.helpers import call_func_by_name
    for ckp in dict1.keys():
        call_func_by_name(sys.modules[__name__], ckp)
