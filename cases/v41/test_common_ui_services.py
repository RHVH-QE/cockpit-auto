import pytest
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_service_page import ServicePage
from fabric.api import run, env, settings
#from cases.v41.test_common_tools import init_browser
from cases import CONF
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


def test_18392(ctx):
    """
    RHEVM-18392
        Check servers status
    """
    log.info("Checking the services")
    try: 
        service_page = ServicePage(ctx)
        service_page.basic_check_elements_exists()
    except AssertionError as e:
        log.exception(e)
        return False
    return True

    log.info("Checking the disable service action...")
    try:
        service_name = service_page.disable_service_action()
        service_page.check_service_is_disabled(service_name)
        log.info("Checking the enable service action...")
        service_page.enable_service_action()
        service_page.check_service_is_enabled(service_name)
        log.info("Checking the stop service action...")
        service_page.stop_service_action()
        service_page.check_service_is_stoped(service_name)
        log.info("Checking the start service action...")
        service_page.start_service_action()
        service_page.check_service_is_started(service_name)
        log.info("Checking the restart service action...")
        service_page.restart_service_action()
        service_page.check_service_is_restarted(service_name)
    except AssertionError as e:
        log.exception(e)
        return False
    return True


def runtest():
    ctx = init_browser()
    test_login(ctx)
    test_18392(ctx)
    ctx.close()
