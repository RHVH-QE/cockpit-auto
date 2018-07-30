import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from avocado import Test
from utils.machine import Machine


OLD_MACHINES_RPM_NAME = ""
NEW_MACHINES_RPM_NAME = ""
BASE_URL = "base/{ver1}/{ver2}/{arch}/{name}"


class TestMachinesLibvirtPackage(Test):
    """
    :avocado: enable
    :avocado: tags=machines_pkg
    """

    def setUp(self):
        host_string = os.environ.get('HOST_STRING')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        self.host = Machine(host_string, username, passwd)
        for rpm_name in [OLD_MACHINES_RPM_NAME, NEW_MACHINES_RPM_NAME]:
            split_dash = rpm_name.split('-')
            split_dot = split_dash[-1].split('.')
            args = {}
            args['ver1'] = split_dash[2]
            args['ver2'] = '.'.join([split_dot[0], split_dot[1]])
            args['arch'] = split_dot[2]
            args['name'] = rpm_name
            url = BASE_URL.format(**args)
            cmd = 'wget {}'.format(url)
            self.host.execute(cmd)

    def test_upgrade_pkg(self):
        cmd = "rpm -i {}".format(OLD_MACHINES_RPM_NAME)
        self.host.execute(cmd)
        cmd = "rpm -U {}".format(NEW_MACHINES_RPM_NAME)
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', NEW_MACHINES_RPM_NAME)

    def test_remove_pkg(self):
        cmd = 'rpm -e cockpit-machines'
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret, '')

    def test_install_pkg(self):
        cmd = 'rpm -i {}'.format(NEW_MACHINES_RPM_NAME)
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', NEW_MACHINES_RPM_NAME)

    def test_start_cockpit(self):
        cmd = 'systemctl enable cockpit.socket && systemctl start cockpit.socket'
        self.host.execute(cmd)
