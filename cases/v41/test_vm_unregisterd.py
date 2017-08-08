from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.vm_page import VirtualMachinesPage
from fabric.api import run, env, settings
from cases import CONF
from cases.v41.test_common_tools import init_browser
#import logging
#import logging.config
#import os

host_ip, host_user, host_password = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password')

env.host_string = host_user + '@' + host_ip
env.password = host_password
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
            request.config._environment.append((
                'redhat-release', redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append((
            'cockpit-ovirt', cockpit_ovirt_version))


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


def test_18803(ctx):
    """
    RHEVM-18803
        Check running VMs (Unregister to RHEVM) status in virtual machines page
    """
    virtual_machines_page = VirtualMachinesPage(ctx)
    virtual_machines_page.basic_check_elements_exists()
    virtual_machines_page.check_running_vms_unregister()


def test_18804(ctx):
    """
    RHEVM-18804
        Check VMs in cluster (Unregister to RHEVM) status in virtual machines page
    """
    virtual_machines_page = VirtualMachinesPage(ctx)
    virtual_machines_page.check_vms_in_cluster_unregister()


def runtest():
    ctx = init_browser()
    test_login(ctx)
    test_18803(ctx)
    test_18804(ctx)
    ctx.close()
