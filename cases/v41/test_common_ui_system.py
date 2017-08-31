import time
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_system_page import SystemPage
from fabric.api import env, run, settings
from cases import CONF
import const
import logging
from print_log import get_current_function_name

log = logging.getLogger("sherry")

dict1 = dict(zip(const.common_ui_system, const.common_ui_system_id))

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
    log.info("Test common_ui_system-->Trying to login to the browser...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)

    
def check_allowunknown_default(ctx):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is default in cockpit
    """
    
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to login into remote machine with 'allowUnknow' is default in cockpit ...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_default()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_allowunknown_true_wrong_account(ctx):
    """
    RHEVM-18381
        Wrong account to login into remote machine
        with "allowUnknow" is true in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Wrong account to login into remote machine with 'allowUnknow' is true in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_wrong_account(second_ip)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_allowunknown_true_remote_closed(ctx):
    """
    RHEVM-18382
        Login remote closed host with "allowUnknow" is true in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to login remote closed host with 'allowUnknow' is true in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_remote_closed(second_ip, "root", second_password)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_allowunknown_true_wrong_address(ctx):
    """
    RHEVM-18383
        Login remote host with wrong address in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to login remote host with wrong address in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_wrong_address()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_allowunknown_true_empty_username(ctx):
    """
    RHEVM-18384
        Login remote host with wrong address in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to login remote host with wrong address in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_empty_username(second_ip, "root", second_password)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_allowunknown_true(ctx):
    """
    RHEVM-18380
        Login into remote machine with "allowUnknown" is true in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to login into remote machine with 'allowUnknow' is true in cockpit ...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true(second_ip, "root", second_password)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_system_login_host(ctx):
    """
    RHEVM-18377
        Login cockpit via Firefox browser
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to login cockpit via Firefox browser...")
        login_page = LoginPage(ctx)
        login_page.basic_check_elements_exists()
        login_page.login_with_incorrect_credential()
        time.sleep(2)
        login_page.login_with_credential(host_user, host_password)
        system_page = SystemPage(ctx)
        system_page.check_login_host(host_ip)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_system_configure_hostname(ctx):
    """
    RHEVM-18385
        Configure hostname
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to configure hostname...")
        system_page = SystemPage(ctx)
        system_page.configure_hostname()
        system_page.check_configure_hostname()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_system_configure_timezone(ctx):
    """
    RHEVM-18386
        Configure timezone
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to configure timezone...")
        system_page = SystemPage(ctx)
        system_page.configure_timezone()
        system_page.check_configure_timezone()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_system_configure_time(ctx):
    """
    RHEVM-18387
        Configure time manually
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to configure time manually...")
        system_page = SystemPage(ctx)
        system_page.configure_time()
        system_page.check_configure_time()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def check_change_system_performance_profile(ctx):
    """
    RHEVM-18390
        Change performance profile
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Trying to change performance profile...")
        system_page = SystemPage(ctx)
        system_page.change_performance_profile()
        system_page.check_change_performance_profile()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def runtest():
    ctx = init_browser()
    #test_login(ctx)
    check_allowunknown_default(ctx)
    check_allowunknown_true(ctx)
    check_allowunknown_true_wrong_account(ctx)
    check_allowunknown_true_remote_closed(ctx)
    check_allowunknown_true_wrong_address(ctx)
    check_allowunknown_true_empty_username(ctx)
    check_system_login_host(ctx)
    check_system_configure_hostname(ctx)
    check_system_configure_timezone(ctx)
    check_system_configure_time(ctx)
    check_change_system_performance_profile(ctx)
    ctx.close()
