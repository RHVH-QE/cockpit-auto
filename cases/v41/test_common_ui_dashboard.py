from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_dashboard_page import DashboardPage
from fabric.api import run, env, settings
from cases import CONF
#from test_common_tools import init_browser
import logging
#import logging.config
#import os
from utils.log import Log

log = Log()


host_ip, host_user, host_password, browser, second_ip, second_password = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('common').get(
            'browser'), CONF.get('hosted_engine').get('second_host'), CONF.get(
                'hosted_engine').get('second_password')

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
            request.config._environment.append(('redhat-release',
                                                redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append(('cockpit-ovirt',
                                            cockpit_ovirt_version))
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


def test_18372(ctx):
    """
    RHEVM-18372
        CPU shown in cockpit page
    """
    log.info("Checking CPU button...")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_cpu()


def test_18373(ctx):
    """
    RHEVM-18373
        Memory shown in cockpit page
    """
    log.info("Checking memory button...")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_memory()


def test_18374(ctx):
    """
    RHEVM-18372
        Network shown in cockpit page
    """
    log.info("Checking network button...")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_network()


def test_18375(ctx):
    """
    RHEVM-18372
        Disk IO shown in cockpit page
    """
    log.info("Checking disk_io button")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_disk_io()


def test_18371(ctx):
    """
    RHEVM-18372
        Servers can be added in Dashboard page
    """
    log.info("Checking whether adding the second host...")
    # To do:
    try:
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_server_can_be_added(second_ip, second_password)
    except Exception as e:
        log.exception(e)
        return False
    return True


def runtest():
    ctx = init_browser()
    test_login(ctx)
    test_18371(ctx)
    test_18372(ctx)
    test_18373(ctx)
    test_18374(ctx)
    test_18375(ctx)
    ctx.close()
