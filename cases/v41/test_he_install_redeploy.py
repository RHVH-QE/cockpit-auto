from selenium import webdriver
from pages.v41.he_install import *
from pages.v41.he_install_auto import *
from fabric.api import env, run, settings
from cases import CONF
from collections import OrderedDict
from utils.helpers import checkpoint
import const
import logging


log = logging.getLogger("sherry")

dict1 = OrderedDict(zip(const.he_install_redeploy, const.he_install_redeploy_id))

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
    else:
        raise NotImplementedError


@checkpoint(dict1)
def check_he_install_redeploy(ctx):
    """
    Purpose:
        RHEVM-18686
        Re-deploy the HostedEngine after clean up the previous HostedEngine
    """
    # Fisrtly to check if there exists HE
    with settings(warn_only=True):
        cmd = "hosted-engine --check-deployed"
        result = run(cmd)
    assert result.failed, "Not support this case since HE is not deployed on %s" % host_ip

    # Cleanup previous HE
    cmd = "vdsClient -s 0 list table | awk '{print $1}' | xargs vdsClient -s 0 destory"
    run(cmd)
    cmd = "rm -rf /etc/vdsm  /etc/ovirt-hosted-engine*"
    run(cmd)
    cmd = "umount -f /rhev/data-center/mnt"
    run(cmd)
    cmd = "rm -rf /rhev/data-center/mnt/*"
    run(cmd)
    cmd = "glusterfs volume stop your_stg"
    run(cmd)
    cmd = "rm -rf /gluster_volume/your_stg/*"
    run(cmd)
    cmd = "glusterfs volume start your_stg"
    run(cmd)

    # Get the nic from host_ip
    cmd = "ip a s|grep %s" % host_ip
    output = run(cmd)
    he_nic = output.split()[-1]

    # Deploy a new HE
    host_dict = {'host_ip': host_ip,
    'host_user': host_user,
    'host_password': host_password}

    nfs_dict = {
    'nfs_ip': nfs_ip,
    'nfs_password': nfs_password,
    'nfs_path': nfs_storage_path}

    install_dict = {
    'rhvm_appliance_path': rhvm_appliance_path,
    'he_nic': he_nic}

    vm_dict = {
    'vm_mac': vm_mac,
    'vm_fqdn': vm_fqdn,
    'vm_ip': vm_ip,
    'vm_password': vm_password,
    'engine_password': engine_password,
    'auto_answer': auto_answer
    }

    log.info("Re-deploy the HostedEngine after clean up the previous HostedEngine...")
    he_install_auto(host_dict, nfs_dict, install_dict, vm_dict)
    # Check the hosted engine is deployed
    check_he_is_deployed(host_ip, host_user, host_password)


def runtest():
    import sys
    from utils.helpers import call_func_by_name
    for ckp in dict1.keys():
        call_func_by_name(sys.modules[__name__], ckp, ctx)
