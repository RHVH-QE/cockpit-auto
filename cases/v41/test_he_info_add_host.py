import time
from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.hosted_engine_page import HePage
from fabric.api import env, run, settings
from utils.helpers import RhevmAction
from cases import CONF
from cases.v41.test_common_tools import init_browser
#import logging
#import logging.config
#import os

host_ip, host_user, host_password, second_host, second_password = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('hosted_engine').get(
            'second_host'), CONF.get('hosted_engine').get('second_password')

he_vm_fqdn, he_vm_ip, he_vm_password = CONF.get('hosted_engine').get(
    'he_vm_fqdn'), CONF.get('hosted_engine').get('he_vm_ip'), CONF.get(
        'hosted_engine').get('he_vm_password')

sd_name, storage_type, storage_addr, storage_pass, storage_path = CONF.get(
    'hosted_engine').get('sd_name'), CONF.get('hosted_engine').get(
        'storage_type'), CONF.get('hosted_engine').get('nfs_ip'), CONF.get(
            'hosted_engine').get('nfs_pass'), CONF.get(
                'hosted_engine').get('he_data_nfs')

env.host_string = host_user + '@' + host_ip
env.password = host_password

he_rhvm = RhevmAction(he_vm_fqdn, "admin", "password")


def check_sd_is_attached(sd_name):
    if he_rhvm.list_storage_domain(sd_name):
        return True


if not check_sd_is_attached(sd_name):
    hosts = he_rhvm.list_all_hosts()
    host_name = hosts["host"][0]["name"]

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
    time.sleep(60)

    he_rhvm.attach_sd_to_datacenter(sd_name=sd_name, dc_name='Default')
    time.sleep(30)


"""
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

"""




def test_login(ctx):
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def test_18668(ctx):
    """
    RHEVM-18668
        Setup additional host
    """
    # Add another host to default DC where also can be running HE
    second_host_name = "cockpit-host"
    he_rhvm.create_new_host(
        ip=second_host,
        host_name=second_host_name,
        password=second_password,
        cluster_name='Default',
        deploy_hosted_engine=True)
    time.sleep(60)

    i = 0
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


def test_18678(ctx):
    """
    RHEVM-18678
        Put the host into local maintenance
    """
    # Put the host to local maintenance
    he_page = HePage(ctx)
    he_page.put_host_to_local_maintenance()
    he_page.check_host_in_local_maintenance()


def test_18679(ctx):
    """
    RHEVM-18679
        Remove the host from maintenance
    """
    he_page = HePage(ctx)

    # Check the host is in local maintenance
    he_page.check_host_in_local_maintenance()

    # Remove the host from local maintenance
    he_page.remove_host_from_local_maintenance()

    # Check the host is in local maintenance
    he_page.check_host_not_in_local_maintenance()


def test_18680(ctx):
    """
    RHEVM-18680
        Put the cluster into global maintenance
    """
    he_page = HePage(ctx)

    # Put the cluster into global maintenance
    he_page.put_cluster_to_global_maintenance()

    # Check the cluster is in global maintenance
    he_page.check_cluster_in_global_maintenance()


def runtest():
    ctx = init_browser()
    test_login(ctx)
    test_18668(ctx)
    test_18678(ctx)
    test_18679(ctx)
    test_18680(ctx)
    ctx.close()
