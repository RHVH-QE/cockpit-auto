from selenium import webdriver
from fabric.api import env, run, settings
from pages.common.nodectl import Nodectl
from cases import CONF
import const
import logging
from print_log import get_current_function_name

log = logging.getLogger("sherry")

dict1 = dict(zip(const.dashboard_nodectl, const.dashboard_nodectl_id))

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
        #return None
    else:
        raise NotImplementedError

def check_nodectl_help_func():
    """
    Purpose:
        RHEVM-18545
        Show nodectl help message in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Test dashboard_nodectl-->Checking nodectl help...")
        nodectl = Nodectl()
        nodectl.check_nodectl_help()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


'''
# Not implemented since no output of "nodectl --version"
def test_18546(firefox):
    """
    Purpose:
        RHEVM-18546
        Check nodectl version in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_version()
'''


def check_nodectl_info_func():
    """
    Purpose:
        RHEVM-18547
        Show information about the image in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking nodectl info...")
        nodectl = Nodectl()
        nodectl.check_nodectl_info(test_build)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


'''
# Not implemented since no update currently
def test_18548(firefox):
    """
    Purpose:
        RHEVM-18548
        Perform an update in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_update()
'''
'''
# Not implemented since no more layer
def test_18549(firefox):
    """
    Purpose:
        RHEVM-18549
        Rollback previous layer in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_rollback()
'''


def check_nodectl_check_func():
    """
    Purpose:
        RHEVM-18550
        Check the system status in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking nodectl check...")
        nodectl = Nodectl()
        nodectl.check_nodectl_check()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_nodectl_debug_func():
    """
    Purpose:
        RHEVM-18551
        Check the debug information of nodectl sub_commands in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking nodectl debug...")
        nodectl = Nodectl()
        nodectl.check_nodectl_debug()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_nodectl_json_func():
    """
    Purpose:
        RHEVM-18552
        Check the JSON output for nodectl in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking nodectl json...")
        nodectl = Nodectl()
        nodectl.check_nodectl_json()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_nodectl_motd_func():
    """
    Purpose:
        RHEVM-18830
        Check the motd for nodectl in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking nodectl motd...")
        nodectl = Nodectl()
        nodectl.check_nodectl_motd()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_nodectl_banner_func():
    """
    Purpose:
        RHEVM-18831
        Check the generate-banner output for nodectl in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Checking nodectl banner...")
        nodectl = Nodectl()
        nodectl.check_nodectl_banner()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def runtest():
    #ctx = init_browser()
    check_nodectl_help_func()
    check_nodectl_info_func()
    check_nodectl_check_func()
    check_nodectl_debug_func()
    check_nodectl_json_func()
    check_nodectl_motd_func()
    check_nodectl_banner_func()
    #ctx.close()
