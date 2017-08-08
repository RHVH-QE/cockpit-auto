from fabric.api import env, run, settings
from pages.common.nodectl import Nodectl
from cases import CONF
from cases.v41.test_common_tools import init_browser
#import logging
#import logging.config
#import os

host_ip, host_user, host_password, test_build = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('test_build')

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


def test_18545(ctx):
    """
    Purpose:
        RHEVM-18545
        Show nodectl help message in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_help()


'''
# Not implemented since no output of "nodectl --version"
def test_18546(firefox):
    """
    Purpose:
        RHEVM-18546
        Check nodectl version in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_version()
'''


def test_18547(ctx):
    """
    Purpose:
        RHEVM-18547
        Show information about the image in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_info(test_build)


'''
# Not implemented since no update currently
def test_18548(firefox):
    """
    Purpose:
        RHEVM-18548
        Perform an update in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_update()
'''
'''
# Not implemented since no more layer
def test_18549(firefox):
    """
    Purpose:
        RHEVM-18549
        Rollback previous layer in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_rollback()
'''


def test_18550(ctx):
    """
    Purpose:
        RHEVM-18550
        Check the system status in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_check()


def test_18551(ctx):
    """
    Purpose:
        RHEVM-18551
        Check the debug information of nodectl sub_commands in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_debug()


def test_18552(ctx):
    """
    Purpose:
        RHEVM-18552
        Check the JSON output for nodectl in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_json()


def test_18830(ctx):
    """
    Purpose:
        RHEVM-18830
        Check the motd for nodectl in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_motd()


def test_18831(ctx):
    """
    Purpose:
        RHEVM-18831
        Check the generate-banner output for nodectl in Terminal
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_banner()


def runtest():
    ctx = init_browser()
    test_18545(ctx)
    test_18547(ctx)
    test_18550(ctx)
    test_18551(ctx)
    test_18552(ctx)
    test_18830(ctx)
    test_18831(ctx)
    ctx.close()
