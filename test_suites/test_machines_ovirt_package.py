import os
import sys
import yaml
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from avocado import Test
from utils.machine import Machine
from utils.caseid import add_case_id 

BASE_URL = "{base}/{ver1}/{ver2}/{arch}/{name}"


class TestMachinesOvirtPackage(Test):
    """
    :avocado: enable
    :avocado: tags=ovirt_pkg
    """

    def setUp(self):
        a = self.get_data('ovirt_package.yml')
        self.config_dict = yaml.load(open(a))
        self.OLD_MACHINES_RPM_NAME = self.config_dict['old_pkg']
        self.NEW_MACHINES_RPM_NAME = self.config_dict['new_pkg']
        self.base = self.config_dict['base_url']

        host_string = os.environ.get('HOST_STRING')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        self.host = Machine(host_string, username, passwd)
        for rpm_name in [self.OLD_MACHINES_RPM_NAME, self.NEW_MACHINES_RPM_NAME]:
            split_dash = rpm_name.split('-')
            split_dot = split_dash[-1].split('.')
            args = {}
            args['base'] = self.base
            args['ver1'] = split_dash[3]
            args['ver2'] = '.'.join([split_dot[0], split_dot[1]])
            args['arch'] = split_dot[2]
            args['name'] = rpm_name
            url = BASE_URL.format(**args)
            cmd = 'curl -o {} {}'.format(rpm_name, url)
            self.host.execute(cmd)

    @add_case_id("RHEL-113962")
    def test_upgrade_pkg(self):
        cmd = 'rpm -e cockpit-machines-ovirt --nodeps'
        self.host.execute(cmd)
        cmd = "rpm -ivh {}".format(self.OLD_MACHINES_RPM_NAME)
        self.host.execute(cmd)
        cmd = "rpm -Uvh {}".format(self.NEW_MACHINES_RPM_NAME)
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines-ovirt --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', self.NEW_MACHINES_RPM_NAME)

    @add_case_id("RHEL-113961")
    def test_remove_pkg(self):
        cmd = 'rpm -e cockpit-machines-ovirt --nodeps'
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines-ovirt'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret, '')

    @add_case_id("RHEL-113768")
    def test_install_pkg(self):
        cmd = 'rpm -ivh {}'.format(self.NEW_MACHINES_RPM_NAME)
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines-ovirt --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', self.NEW_MACHINES_RPM_NAME)
        cmd = 'systemctl enable cockpit.socket && systemctl start cockpit.socket'
        self.host.execute(cmd)
