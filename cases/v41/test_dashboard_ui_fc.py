from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.dashboard_nodestatus_page import NodeStatusPage
from fabric.api import env, run, settings
from cases import CONF
import const
import logging
from print_log import get_current_function_name

log = logging.getLogger("sherry")



dict1 = dict(zip(const.dashboard_ui_fc, const.dashboard_ui_fc_id))

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
        #return None
    else:
        raise NotImplementedError

def test_login(ctx):
    log.info("Test dashboard_ui_fc-->Trying to login to cockpit...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


# This will be tested on a rhvh with FC
def check_nodestatus_fc(ctx):
    """
    RHEVM-18538
        Check node status with FC multipath.
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking node status with FC multipath...")
        node_status_page = NodeStatusPage(ctx)
        test_layer = test_build + '+1'
        node_status_page.check_node_status_fc(test_layer)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def runtest():
    ctx = init_browser()
    test_login(ctx)
    check_nodestatus_fc(ctx)
    ctx.close()
