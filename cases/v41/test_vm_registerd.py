import time
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.vm_page import VirtualMachinesPage
from pages.common.dashboard_nodestatus_page import NodeStatusPage
from fabric.api import run, env, settings
from utils.helpers import RhevmAction
from cases import CONF
from cases.v41.test_common_tools import init_browser
#import logging
#import logging.config
#import os

host_ip, host_user, host_password = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password')

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

he_rhvm = RhevmAction(he_vm_fqdn, "admin", "password")


def check_sd_is_attached(sd_name):
    if he_rhvm.list_storage_domain(sd_name):
        return True


def check_new_vm_exists(vm_name):
    if he_rhvm.list_vm(vm_name):
        return True


if not check_sd_is_attached(sd_name):
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

if not check_new_vm_exists(second_vm_fqdn):
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
"""
@pytest.fixture(scope="session", autouse=True)
def _environment(request):
    with settings(warn_only=True):
        cmd = "rpm -qa|grep cockpit-ovirt"
        cockpit_ovirt_version = run(cmd)

        cmd = "rpm -q imgbased"
        result = run(cmd)
        if result.failed:
            cmd = "cat /etc/redhat-release"
            redhat_release = run(cmd)
            request.config._environment.append(('redhat-release',
                                                redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append(('cockpit-ovirt',
                                            cockpit_ovirt_version))


@pytest.fixture(scope="module")
def firefox(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    driver.close()
"""


def test_login(ctx):
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def test_18805(ctx):
    """
    RHEVM-18805
        Check running VMs (Register to RHEVM) status in virtual machines page
        Suppose there are two vms including HE vm and another commom vm
    """
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_running_vms_register(he_vm_fqdn, he_vm_ip, he_vm_password,
                                       second_vm_fqdn)


def test_18808(ctx):
    """
    RHEVM-18808
        Check VDSM info in virtual machines page
    """
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_vdsm_elements()
    vm_page.check_vdsm_conf_edit()
    vm_page.check_vdsm_conf_save()
    vm_page.check_vdsm_conf_reload()


def test_18809(ctx):
    """
    RHEVM-18809
        Check Login to Engine in virtual machines page
    """
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_vm_login_to_engine(he_vm_fqdn, he_engine_password)
    time.sleep(2)
    vm_page.check_vm_logout_from_engine()


def test_18811(ctx):
    """
    RHEVM-18811
        Check Refresh in virtual machines page
    """
    vm_page = VirtualMachinesPage(ctx)
    vm_page.check_vm_refresh()


def test_18813(ctx):
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
    # Logout the non-root account from cockpit
    vm_page = VirtualMachinesPage(ctx)
    vm_page.logout_from_cockpit()

    # Login with root account
    login_page = LoginPage(ctx)
    login_page.login_with_credential(host_user, host_password)


def runtest():
    ctx = init_browser()
    test_login(ctx)
    test_18805(ctx)
    test_18808(ctx)
    test_18809(ctx)
    test_18811(ctx)
    test_18813(ctx)
    test_login_again(ctx)
    ctx.close()
