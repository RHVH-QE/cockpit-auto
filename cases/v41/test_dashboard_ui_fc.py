from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.common.dashboard_nodestatus_page import NodeStatusPage
from fabric.api import env, run, settings
from cases import CONF
from cases.v41.test_common_tools import init_browser
#import logging
#import logging.config
#import os

host_ip, host_user, host_password, test_build, rhvm_fqdn = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('common').get(
            'test_build'), CONF.get('common').get('rhvm_fqdn')

env.host_string = host_user + '@' + host_ip
env.password = host_password
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
            request.config._environment.append((
                'redhat-release', redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append((
            'cockpit-ovirt', cockpit_ovirt_version))
"""


def test_login(ctx):
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


# This will be tested on a rhvh with FC
def test_18538(ctx):
    """
    RHEVM-18538
        Check node status with FC multipath.
    """
    node_status_page = NodeStatusPage(ctx)
    test_layer = test_build + '+1'
    node_status_page.check_node_status_fc(test_layer)


def runtest():
    ctx = init_browser()
    test_login(ctx)
    test_18538(ctx)
    ctx.close()
