import time
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.vm_page import VirtualMachinesPage
from pages.v41.dashboard_nodestatus_page import NodeStatusPage
from fabric.api import run, env, settings
from utils.rhvmapi import RhevmAction
from cases import CONF
from collections import OrderedDict
from utils.helpers import checkpoint
import const
import logging


log = logging.getLogger("sherry")

dict1 = OrderedDict(zip(const.vm_registerd, const.vm_registerd_id))

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')

he_vm_fqdn, he_vm_ip, he_vm_password, he_engine_password, second_vm_fqdn = CONF.get(
    'hosted_engine').get('he_vm_fqdn'), CONF.get('hosted_engine').get(
        'he_vm_ip'), CONF.get('hosted_engine').get('he_vm_password'), CONF.get(
            'hosted_engine').get('engine_password'), CONF.get(
                'hosted_engine').get('second_host_fqdn')

sd_name, storage_type, storage_addr, storage_pass, storage_path = CONF.get(
    'hosted_engine').get('sd_name'), CONF.get('hosted_engine').get(
        'storage_type'), CONF.get('hosted_engine').get('nfs_ip'), CONF.get(
            'hosted_engine').get('nfs_pass'), CONF.get('hosted_engine').get(
                'he_data_nfs')

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


def test_login(ctx):
    log.info("Trying to login to cockpit...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


@checkpoint(dict1)
def check_running_vms_register_func(ctx):
    """
    RHEVM-18805
        Check running VMs (Register to RHEVM) status in virtual machines page
        Suppose there are two vms including HE vm and another commom vm
    """
    log.info('Check running VMs (Register to RHEVM) status in virtual machines page...')
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_running_vms_register(he_vm_fqdn, he_vm_ip, he_vm_password,
                                    second_vm_fqdn)


@checkpoint(dict1)
def check_vdsm_func(ctx):
    """
    RHEVM-18808
        Check VDSM info in virtual machines page
    """
    log.info("Check VDSM info in virtual machines page...")
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_vdsm_elements()
    vm_page.check_vdsm_conf_edit()
    vm_page.check_vdsm_conf_save()
    vm_page.check_vdsm_conf_reload()


@checkpoint(dict1)
def check_vm_login_logout_engine_func(ctx):
    """
    RHEVM-18809
        Check Login to Engine in virtual machines page
    """
    log.info("Check Login to Engine in virtual machines page...")
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_vm_login_to_engine(he_vm_fqdn, he_engine_password)
    time.sleep(2)
    vm_page.check_vm_logout_from_engine()


@checkpoint(dict1)
def check_vm_refresh_func(ctx):
    """
    RHEVM-18811
        Check Refresh in virtual machines page
    """
    log.info("Check Refresh in virtual machines page")
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_vm_refresh()


@checkpoint(dict1)
def check_non_root_alert_func(ctx):
    """
    RHEVM-18813
        Check VM page with non-root account
    """
    # Add non-root user and password
    test_user = "cockpit"
    test_password = "cockpit"

    # Check whether test_user exists
    with settings(warn_only=True):
        cmd = "id %s" % test_user
        output = run(cmd)
        if output.failed:
            cmd = "useradd %s" % test_user
            run(cmd)
        cmd = "echo %s | passwd --stdin %s" % (test_password, test_user)
        run(cmd)

    # Logout the root account from cockpit
    log.info("Check VM page with non-root account")
    vm_page = VirtualMachinesPage(ctx)
    vm_page.logout_from_cockpit()

    # Login with non-root account
    login_page = LoginPage(ctx)
    login_page.login_with_credential(test_user, test_password)

    # Check if there is "Can't check node status!
    # "Please run as an administrator!"
    node_status_page = NodeStatusPage(ctx)
    node_status_page.check_non_root_alert(default=True)


def test_login_again(ctx):
    log.info("Trying to test login to cockpit again...")
    # Logout the non-root account from cockpit
    vm_page = VirtualMachinesPage(ctx)
    vm_page.logout_from_cockpit()

    # Login with root account
    login_page = LoginPage(ctx)
    login_page.login_with_credential(host_user, host_password)


def add_sd(he_rhvm, sd_name):
    if not he_rhvm.list_storage_domain(sd_name):
        # Get the host name added to the hosted engine
        with settings(warn_only=True):
            host_name = run("hostname")

        # Clean the nfs path
        cmd = "rm -rf %s/*" % storage_path
        with settings(
                warn_only=True,
                host_string='root@' + storage_addr,
                password=storage_pass):
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

        he_rhvm.attach_sd_to_datacenter(sd_name=sd_name, dc_name='Default')


def add_vm(he_rhvm, second_vm_fqdn):
    if not he_rhvm.list_vm(second_vm_fqdn):
        # Create new vm without installing guest os under Default DC
        he_rhvm.create_vm(vm_name=second_vm_fqdn, cluster="Default")
        time.sleep(30)

        # Create a disk for vm
        disk_name = "hevm_disk"
        disk_size = "30589934592"
        he_rhvm.create_vm_image_disk(second_vm_fqdn, sd_name, disk_name, disk_size)
        time.sleep(60)

        # Startup the vm
        he_rhvm.operate_vm(vm_name=second_vm_fqdn, operation="start")
        time.sleep(60)
        i = 0
        while True:
            if i > 30:
                assert 0, "Vm not up after creation"
            vm_status = he_rhvm.list_vm(second_vm_fqdn)['status']
            if vm_status == "up":
                break
            time.sleep(10)
            i += 1


def runtest():
    he_rhvm = RhevmAction(he_vm_fqdn, "admin", "password")
    add_sd(he_rhvm, sd_name)
    add_vm(he_rhvm, second_vm_fqdn)

    ctx = init_browser()
    test_login(ctx)
    import sys
    from utils.helpers import call_func_by_name
    for ckp in dict1.keys():
        call_func_by_name(sys.modules[__name__], ckp, ctx)
    ctx.close()
