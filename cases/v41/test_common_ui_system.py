import time
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_system_page import SystemPage
from fabric.api import env, run, settings
from cases import CONF
#from cases.v41.test_common_tools import init_browser
import logging
import logging.config
import os

dirname = os.path.dirname(os.path.dirname(__file__))
conf_path = os.path.join(dirname + "/logger.conf")
logging.config.fileConfig(conf_path)
log = logging.getLogger("sherry")

host_ip, host_user, host_password, second_ip, second_password, browser = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('hosted_engine').get(
            'second_host'), CONF.get('hosted_engine').get(
                'second_password'), CONF.get('common').get('browser')

env.host_string = host_user + '@' + host_ip
env.password = host_password
"""
def _environment(request):
    with settings(warn_only=True):
        cmd = "rpm -qa|grep cockpit-ovirt"
        cockpit_ovirt_version = run(cmd)

        cmd = "rpm -q imgbased"
        result = run(cmd)
        if result.failed:
            cmd = "cat /etc/redhat-release"
            redhat_release = run(cmd)
            request.config._environment.append((
                'redhat-release', redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append((
            'cockpit-ovirt', cockpit_ovirt_version))
"""

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
        #return None
    else:
        raise NotImplementedError

def test_login(ctx):
    log.info("Trying to login to the browser...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)

    
def test_18379(ctx):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is default in cockpit
    """
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_default()


def test_18381(ctx):
    """
    RHEVM-18381
        Wrong account to login into remote machine
        with "allowUnknow" is true in cockpit
    """
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_wrong_account(second_ip)


def test_18382(ctx):
    """
    RHEVM-18382
        Login remote closed host with "allowUnknow" is true in cockpit
    """
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_remote_closed(second_ip, "root",
                                                      second_password)


def test_18383(ctx):
    """
    RHEVM-18383
        Login remote host with wrong address in cockpit
    """
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_wrong_address()


def test_18384(ctx):
    """
    RHEVM-18384
        Login remote host with wrong address in cockpit
    """
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_empty_username(second_ip, "root",
                                                       second_password)


def test_18380(ctx):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is true in cockpit
    """
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true(second_ip, "root", second_password)


def test_18377(ctx):
    """
    RHEVM-18377
        Login cockpit via Firefox browser
    """
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_incorrect_credential()
    time.sleep(2)
    login_page.login_with_credential(host_user, host_password)
    system_page = SystemPage(ctx)
    system_page.check_login_host(host_ip)


def test_18385(ctx):
    """
    RHEVM-18385
        Configure hostname
    """
    system_page = SystemPage(ctx)
    system_page.configure_hostname()
    system_page.check_configure_hostname()


def test_18386(ctx):
    """
    RHEVM-18386
        Configure timezone
    """
    system_page = SystemPage(ctx)
    system_page.configure_timezone()
    system_page.check_configure_timezone()


def test_18387(ctx):
    """
    RHEVM-18386
        Configure time manually
    """
    system_page = SystemPage(ctx)
    system_page.configure_time()
    system_page.check_configure_time()


def test_18390(ctx):
    """
    RHEVM-18386
        Change performance profile
    """
    system_page = SystemPage(ctx)
    system_page.change_performance_profile()
    system_page.check_change_performance_profile()


def runtest():
    ctx = init_browser()
    test_18379(ctx)
    #test_18380(ctx)
    #test_18381(ctx)
    #test_18382(ctx)
    #test_18383(ctx)
    #test_18384(ctx)
    #test_18377(ctx)
    #test_18385(ctx)
    #test_18385(ctx)
    #test_18386(ctx)
    #test_18387(ctx)
    #test_18390(ctx)
    ctx.close()
