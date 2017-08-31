from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_service_page import ServicePage
from fabric.api import run, env, settings
import const
import logging
from print_log import get_current_function_name
from cases import CONF

log = logging.getLogger("sherry")

dict1 = dict(zip(const.common_ui_services, const.common_ui_services_id))

host_ip, host_user, host_password, second_ip, second_password, browser = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('hosted_engine').get(
            'second_host'), CONF.get('hosted_engine').get(
                'second_password'), CONF.get('common').get('browser')

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
        #return None
    else:
        raise NotImplementedError

def test_login(ctx):
    log.info("Test common_ui_services-->Trying to login to the browser...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def check_ui_services(ctx):
    """
    RHEVM-18392
        Check servers status
    """
    log.info("Checking the services")
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking the services")
        service_page = ServicePage(ctx)
        service_page.basic_check_elements_exists()
        log.info("Checking the disable service action...")
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
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except AssertionError as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
    


def runtest():
    ctx = init_browser()
    test_login(ctx)
    check_ui_services(ctx)
    ctx.close()
