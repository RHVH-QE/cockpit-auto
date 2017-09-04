import time
import re
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.hosted_engine_page import HePage
from fabric.api import env, run, settings
from fabric.operations import reboot
from cases import CONF
import const
from utils.helpers import get_cur_func
import logging

log = logging.getLogger("sherry")

dict1 = dict(zip(const.he_info, const.he_info_id))

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')

he_vm_fqdn, he_vm_ip, he_vm_password, engine_password, he_data_nfs, second_vm_fqdn = CONF.get(
    'hosted_engine').get('he_vm_fqdn'), CONF.get('hosted_engine').get(
        'he_vm_ip'), CONF.get('hosted_engine').get('he_vm_password'), CONF.get(
            'hosted_engine').get('engine_password'), CONF.get(
                'hosted_engine').get('he_data_nfs'), CONF.get(
                    'hosted_engine').get('second_vm_fqdn')

env.host_string = host_user + '@' + host_ip
env.password = host_password

# Reboot the host before test
with settings(warn_only=True):
    reboot(wait=600)
time.sleep(300)

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
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def check_engine_status_func(ctx):
    """
    RHEVM-18669
        Hosted Engine status can be checked after configuration
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        he_page = HePage(ctx)
        he_page.check_engine_status()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_vm_status_func(ctx):
    """
    RHEVM-18670
        Check the vm still up after reboot node
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        he_page = HePage(ctx)
        # Check engine status
        he_page.check_engine_status()
        # Check VM state
        he_page.check_vm_status()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_three_buttons_func(ctx):
    """
    RHEVM-18671
        Reboot RHVH after finished configure hosted engine
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        he_page = HePage(ctx)

        # Check engine status
        he_page.check_engine_status()
        time.sleep(2)

        # Check three maintenance buttons exist
        he_page.check_three_buttons()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_he_running_on_host_func(ctx):
    """
    RHEVM-18672
        Verify hosted-engine cockpit show correct info after setup hosted engine with OVA
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        he_page = HePage(ctx)
        # Check engine status
        he_page.check_engine_status()

        # Check three maintenance buttons exist
        he_page.check_he_running_on_host(host_ip)

        # Check vm statues
        he_page.check_vm_status()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


'''
def test_18684(firefox):
    """
    RHEVM-18684
        Check if there are a large number of redundant log generation in /var/log/messages
    """
    # To Do
    pass
'''


def check_no_password_saved_func(ctx):
    """
    RHEVM-18685
        Check there is no Hosted Engine passwords are saved in the logs as clear text
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        # Find the hosted engine setup log
        cmd = "find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log"
        output_log = run(cmd)

        # Find the line contains "Enter engine admin password"
        cmd = "grep 'Enter engine admin password' %s" % output_log
        with settings(warn_only=True):
            output_password = run(cmd)

        output_password = output_password.split(':')[-1]
        assert not re.search(engine_password, output_password),     \
            "Hosted engine password is saved in the logs as clear text"
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def runtest():
    ctx = init_browser()
    check_engine_status_func(ctx)
    check_vm_status_func(ctx)
    check_three_buttons_func(ctx)
    check_he_running_on_host_func(ctx)
    check_no_password_saved_func(ctx)
    ctx.close()
