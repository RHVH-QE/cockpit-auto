from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_dashboard_page import DashboardPage
from fabric.api import run, env, settings
from cases import CONF
import logging
import const

from print_log import get_current_function_name

dict1 = dict(zip(const.common_ui_dashboard, const.common_ui_dashboard_id))

log = logging.getLogger("sherry")



host_ip, host_user, host_password, browser, second_ip, second_password = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('common').get(
            'browser'), CONF.get('hosted_engine').get('second_host'), CONF.get(
                'hosted_engine').get('second_password')

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
    log.info("Test common_ui_dashboard-->Trying to login to the browser...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def check_dashboard_cpu(ctx):
    """
    RHEVM-18372
        CPU shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking CPU button...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_cpu()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)

    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
       

def check_dashboard_memory(ctx):
    """
    RHEVM-18373
        Memory shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking memory button...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_memory()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_dashboard_network(ctx):
    """
    RHEVM-18374
        Network shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking network button...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_network()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_dashboard_disk_io(ctx):
    """
    RHEVM-18372
        Disk IO shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking disk_io button")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_disk_io()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_another_server(ctx):
    """
    RHEVM-18372
        Servers can be added in Dashboard page
    """
    
    # To do:
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking whether adding the second host...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_server_can_be_added(second_ip, second_password)
        log.info('func_(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func_(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
        return False
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        #return False
    return True
    


def runtest():
    ctx = init_browser()
    test_login(ctx)
    check_another_server(ctx)
    check_dashboard_cpu(ctx)
    check_dashboard_memory(ctx)
    check_dashboard_network(ctx)
    check_dashboard_disk_io(ctx)
    ctx.close()
