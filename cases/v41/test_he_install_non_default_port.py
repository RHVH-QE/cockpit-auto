from pages.common.he_install import *
from fabric.api import env, run, settings
from cases import CONF
from cases.v41.test_common_tools import init_browser
#import logging
#import logging.config
#import os

host_ip, host_user, host_password = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password')

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
    pass
"""

def test_18667(ctx):
    """
    Purpose:
        RHEVM-18667
        Verify to deploy Hosted-Engine via non-default cockpit port
    """
    # Check the cockpit is active
    cmd = "systemctl status cockpit|grep Active"
    output = run(cmd)
    status = output.split()[1]
    assert status == "active", "Cockpit dameon is not active"

    # Check cockpit packages
    cmd = "cockpit-bridge --packages"
    output = run(cmd)
    assert output, "Cockpit packages not exist"

    # Modify the default cockpit port
    cmd = "sed -i 's/ListenStream=9090/ListenStream=9898/'"
    run(cmd)

    # Add port to firewall
    cmd = "firewall-cmd --add-port=9898/tcp"
    run(cmd)

    # Add to permanent
    cmd = "firewall-cmd --permanent --add-port=9898/tcp"
    run(cmd)

    # SElinux operation
    cmd = "semanage port -a -t websm_port_t -p tcp 9898"
    run(cmd)

    # Reload the dameon
    cmd = "systemctl daemon-reload"
    run(cmd)

    # Restart the cockpit
    cmd = "systemctl restart cockpit.socket"
    run(cmd)
    time.sleep(5)

    # Get the nic from host_ip
    cmd = "ip a s|grep %s" % host_ip
    output = run(cmd)
    he_nic = output.split()[-1]

    host_dict = {
    'host_ip': host_ip,
    'host_user': host_user,
    'host_password': host_password,
    'cockpit_port': '9898'}

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

    he_install(host_dict, nfs_dict, install_dict, vm_dict)

    # Check the hosted engine is deployed
    check_he_is_deployed(host_ip, host_user, host_password)

def runtest():
    ctx = init_browser()
    test_18667(ctx)
    ctx.close()
