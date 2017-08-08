from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_log_page import LogPage
from fabric.api import run, env, settings
from cases import CONF
#from test_common_tools import init_browser
import logging
import logging.config
import os

dirname = os.path.dirname(os.path.dirname(__file__))
conf_path = os.path.join(dirname + "/logger.conf")
logging.config.fileConfig(conf_path)
log = logging.getLogger("sherry")

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')

env.host_string = host_user + '@' + host_ip
env.password = host_password


"""
def _environment(request):
    with settings(warn_only=True):
        cmd = "rpm -q cockpit-ovirt-dashboard"
        cockpit_ovirt_version = run(cmd)
        print cockpit_ovirt_version
        request.config._environment.append(('cockpit-ovirt',
                                            cockpit_ovirt_version))

        cmd = "rpm -q imgbased"
        result = run(cmd)
        if result.failed:
            cmd = "cat /etc/redhat-release"
            redhat_release = run(cmd)
            request.config._environment.append(('redhat-release',
                                                redhat_release))
        else:
            cmd = "imgbase w"
            output_imgbase = run(cmd)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))
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
    log.info("Checking the logs...")
    try:
        log_page = LogPage(ctx)
        log_page.basic_check_elements_exists()
        log.info("Checking the recent logs...")
        log_page.check_recent_logs()
        log.info("Checking the current logs...")
        log_page.check_current_boot_logs()
        log.info("Checking the last 24h logs...")
        log_page.check_last_24hours_logs()
        log.info("Checking the last 7d logs...")
        log_page.check_last_7days_logs()
    except Exception as e:
        log.exception(e)
        return False
    return True

def runtest():
    ctx = init_browser()
    test_login(ctx)
    test_18392(ctx)
    ctx.close()
