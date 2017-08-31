import time
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.hosted_engine_page import HePage
from fabric.api import env, run, settings
from utils.rhvmapi import RhevmAction
from cases import CONF
#from cases.v41.test_common_tools import init_browser
import const
import logging
from print_log import get_current_function_name

log = logging.getLogger("sherry")

dict1 = dict(zip(const.he_info_add_host, const.he_info_add_host_id))

host_ip, host_user, host_password, second_host, second_password, browser = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('hosted_engine').get(
            'second_host'), CONF.get('hosted_engine').get(
                'second_password'), CONF.get('common').get('browser')

he_vm_fqdn, he_vm_ip, he_vm_password = CONF.get('hosted_engine').get(
    'he_vm_fqdn'), CONF.get('hosted_engine').get('he_vm_ip'), CONF.get(
        'hosted_engine').get('he_vm_password')

sd_name, storage_type, storage_addr, storage_pass, storage_path = CONF.get(
    'hosted_engine').get('sd_name'), CONF.get('hosted_engine').get(
        'storage_type'), CONF.get('hosted_engine').get('nfs_ip'), CONF.get(
            'hosted_engine').get('nfs_pass'), CONF.get('hosted_engine').get(
                'he_data_nfs')

env.host_string = host_user + '@' + host_ip
env.password = host_password

he_rhvm = RhevmAction(he_vm_fqdn, "admin", "password")


def check_sd_is_attached(sd_name):
    if he_rhvm.list_storage_domain(sd_name):
        return True


if not check_sd_is_attached(sd_name):
    log.info("Creating the nfs storage...")
    hosts = he_rhvm.list_all_hosts()
    host_name = hosts["host"][0]["name"]

    # Clean the nfs path

    with settings(warn_only=True, host_string='root@' + storage_addr, password=storage_pass):
        cmd = "rm -rf %s/*" % storage_path
        run(cmd)

    # Add nfs storage to Default DC on Hosted Engine,
    # which is used for creating vm
    
    he_rhvm.create_plain_storage_domain(
        sd_name=sd_name,
        sd_type='data',
        storage_type=storage_type,
        storage_addr=storage_addr,
        storage_path=storage_path,
        host=host_name)
    time.sleep(60)
    
    log.info("Attaching sd to datacenter...")
    he_rhvm.attach_sd_to_datacenter(sd_name=sd_name, dc_name='Default')
    time.sleep(30)
    

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
    log.info("Trying to logining to Cockpit...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def check_add_additional_host():
    """
    RHEVM-18668
        Setup additional host
    """
    # Add another host to default DC where also can be running HE
    log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
    log.info("Setup another host to default DC...")
    second_host_name = "cockpit-host"
    he_rhvm.create_new_host(
        ip=second_host,
        host_name=second_host_name,
        password=second_password,
        cluster_name='Default',
        deploy_hosted_engine=True)
    time.sleep(60)

    i = 0
    try:
        while True:
            if i > 65:
                assert 0, "Timeout waitting for host is up"
            host_status = he_rhvm.list_host(second_host_name)['status']
            if host_status == 'up':
                break
            elif host_status == 'install_failed':
                assert 0, "Host is not up as current status is: %s" % host_status
            elif host_status == 'non_operational':
                assert 0, "Host is not up as current status is: %s" % host_status
            time.sleep(10)
            i += 1
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_put_local_maintenance(ctx):
    """
    RHEVM-18678
        Put the host into local maintenance
    """
    # Put the host to local maintenance
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        log.info("Putting the host into local maintenance...")
        he_page = HePage(ctx)
        he_page.put_host_to_local_maintenance()
        log.info("Checking the host local_maintenance...")
        he_page.check_host_in_local_maintenance()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_remove_from_maintenance(ctx):
    """
    RHEVM-18679
        Remove the host from maintenance
    """
    # Check the host is in local maintenance
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        he_page = HePage(ctx)
        he_page.check_host_in_local_maintenance()
        log.info("Removing host from local_maintenance...")
        he_page.remove_host_from_local_maintenance()
        log.info("Checking host removed from local_maintenance...")
        he_page.check_host_not_in_local_maintenance()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])


def check_put_global_maintenance(ctx):
    """
    RHEVM-18680
        Put the cluster into global maintenance
    """

    # Check the cluster is in global maintenance
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])
        he_page = HePage(ctx)
        log.info("Putting cluster to global maintenance...")
        he_page.put_cluster_to_global_maintenance()
        log.info("Checking cluster in global maintenance...")
        he_page.check_cluster_in_global_maintenance()
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_current_function_name(),dict1[get_current_function_name()]))
        log.error(e)
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_current_function_name()])

def runtest():
    #test_18668()
    ctx = init_browser()
    check_add_additional_host()
    test_login(ctx)
    check_put_local_maintenance(ctx)
    check_remove_from_maintenance(ctx)
    check_put_global_maintenance(ctx)
    ctx.close()
