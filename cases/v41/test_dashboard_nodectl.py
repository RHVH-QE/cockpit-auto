from selenium import webdriver
from fabric.api import env, run, settings
from pages.v41.nodectl import Nodectl
from cases import CONF
import logging
import const
from utils.helpers import get_cur_func

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
    else:
        raise NotImplementedError


def check_nodectl_help_func():
    """
    Purpose:
        RHEVM-18545
        Show nodectl help message in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Test dashboard_nodectl-->Checking nodectl help...")
        nodectl = Nodectl()
        nodectl.check_nodectl_help()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else: 
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_nodectl_info_func():
    """
    Purpose:
        RHEVM-18547
        Show information about the image in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking nodectl info...")
        nodectl = Nodectl()
        nodectl.check_nodectl_info(test_build)
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_nodectl_check_func():
    """
    Purpose:
        RHEVM-18550
        Check the system status in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking nodectl check...")
        nodectl = Nodectl()
        nodectl.check_nodectl_check()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_nodectl_debug_func():
    """
    Purpose:
        RHEVM-18551
        Check the debug information of nodectl sub_commands in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking nodectl debug...")
        nodectl = Nodectl()
        nodectl.check_nodectl_debug()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_nodectl_json_func():
    """
    Purpose:
        RHEVM-18552
        Check the JSON output for nodectl in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking nodectl json...")
        nodectl = Nodectl()
        nodectl.check_nodectl_json()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_nodectl_motd_func():
    """
    Purpose:
        RHEVM-18830
        Check the motd for nodectl in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking nodectl motd...")
        nodectl = Nodectl()
        nodectl.check_nodectl_motd()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_nodectl_banner_func():
    """
    Purpose:
        RHEVM-18831
        Check the generate-banner output for nodectl in Terminal
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking nodectl banner...")
        nodectl = Nodectl()
        nodectl.check_nodectl_banner()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def runtest():
    check_nodectl_help_func()
    check_nodectl_info_func()
    check_nodectl_check_func()
    check_nodectl_debug_func()
    check_nodectl_json_func()
    check_nodectl_motd_func()
    check_nodectl_banner_func()
