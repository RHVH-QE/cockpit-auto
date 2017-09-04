from selenium import webdriver
from pages.v41.he_install import *
from pages.v41.he_install_auto import *
from fabric.api import env, run, settings
from cases import CONF
import const
from utils.helpers import get_cur_func
import logging

log = logging.getLogger("sherry")

dict1 = dict(zip(const.he_install, const.he_install_id))

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')

nfs_ip, nfs_password, nfs_storage_path, rhvm_appliance_path, vm_mac, vm_fqdn, vm_ip, vm_password, engine_password, auto_answer = CONF.get(
    'hosted_engine'
).get('nfs_ip'), CONF.get('hosted_engine').get('nfs_password'), CONF.get(
    'hosted_engine'
).get('he_install_nfs'), CONF.get('hosted_engine').get(
    'rhvm_appliance_path'
), CONF.get('hosted_engine').get('he_vm_mac'), CONF.get('hosted_engine').get(
    'he_vm_fqdn'), CONF.get('hosted_engine').get('he_vm_ip'), CONF.get(
        'hosted_engine').get('he_vm_password'), CONF.get('hosted_engine').get(
            'engine_password'), CONF.get('hosted_engine').get('auto_answer')

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

def check_he_install_bond(ctx):
    """
    Purpose:
        RHEVM-18674
        Setup hosted engine through ova with bond as network
    """
    # Get the bond device
    with settings(warn_only=True):
        cmd = "ls /etc/sysconfig/network-scripts | egrep 'ifcfg-bond[0-9]$' | awk -F '-' '{print $2}'"
        ret = run(cmd)
    if ret.failed:
        assert 0, "Not support this case since no bond device found"
    he_nic = ret

    # get ip addr
    with settings(warn_only=True):
        cmd = "ip -f inet addr show %s|grep inet|awk '{print $2}'|awk -F'/' '{print $1}'" % he_nic
        ret = run(cmd)
    if ret.failed:
        assert 0, "Not support this case since bond has no ip address configured"

    host_dict = {
        'host_ip': host_ip,
        'host_user': host_user,
        'host_password': host_password
    }

    nfs_dict = {
        'nfs_ip': nfs_ip,
        'nfs_password': nfs_password,
        'nfs_path': nfs_storage_path
    }

    install_dict = {
        'rhvm_appliance_path': rhvm_appliance_path,
        'he_nic': he_nic
    }

    vm_dict = {
        'vm_mac': vm_mac,
        'vm_fqdn': vm_fqdn,
        'vm_ip': vm_ip,
        'vm_password': vm_password,
        'engine_password': engine_password,
        'auto_answer': auto_answer
    }
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Setup hosted engine through ova with bond as network...")
        he_install_auto(host_dict, nfs_dict, install_dict, vm_dict)
        
        # Check the hosted engine is deployed
        check_he_is_deployed(host_ip, host_user, host_password)
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def runtest():
    ctx = init_browser()
    check_he_install_bond(ctx)
    ctx.close()
