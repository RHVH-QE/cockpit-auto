from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.ui_log_page import LogPage
from fabric.api import run, env, settings
from cases import CONF
import const
import logging
from print_log import get_current_function_name

log = logging.getLogger("sherry")

dict1 = dict(zip(const.common_ui_logs, const.common_ui_logs_id))

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')

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
    log.info("Test commom_ui_log-->Trying to login to the browser...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def check_ui_logs(ctx):
    """
    RHEVM-18394
        Check servers status
    """
    
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking the logs...")
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
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
    

def runtest():
    ctx = init_browser()
    test_login(ctx)
    check_ui_logs(ctx)
    ctx.close()
