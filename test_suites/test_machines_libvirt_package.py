import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from avocado import Test
from utils.machine import Machine
from utils.caseid import add_case_id, check_case_id

URL_VER = "/{ver1}/{ver2}/{arch}/{name}"


class TestMachinesLibvirtPackage(Test):
    """
    :avocado: enable
    :avocado: tags=machines_pkg
    """

    def setUp(self):
        # initialize polarion case
        self.case_id = None
        self.case_state = None

        host_string = os.environ.get('HOST_STRING')
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        self.host = Machine(host_string, username, passwd)
        self.new_ver = self.params.get('new_machines_rpm_ver')
        # put repo file
        if "el7" in self.new_ver:
            repo_file_name = "mc_7.repo"
        else:
            repo_file_name = "mc_n.repo"
        cmd = 'test -e /etc/yum.repos.d/{}'.format(repo_file_name)
        ret = self.host.execute(cmd, raise_exception=False)
        if not ret.succeeded:
            repo_file_path = self.get_data(repo_file_name)
            self.host.put_file(repo_file_path, "/etc/yum.repos.d/")

    @check_case_id
    def tearDown(self):
        pass

    @add_case_id("RHEL-113808")
    def test_install_pkg(self):
        cmd = 'yum install -y cockpit-machines'
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', self.new_ver)

    @add_case_id("RHEL-115592")
    def test_remove_pkg(self):
        """
        :avocado: tags=test
        """
        cmd = 'yum remove -y cockpit-machines'
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret, '')

    @add_case_id("RHEL-114013")
    def test_update_pkg(self):
        old_ver = self.params.get('old_machines_rpm_ver')
        if 'el7' in old_ver:
            base_url = self.params.get('base_url_7')
        else:
            base_url = self.params.get('base_url_n')
        # download old ver
        cmd = 'test -e {}'.format(old_ver)
        ret = self.host.execute(cmd, raise_exception=False)
        if not ret.succeeded:
            split_dash = old_ver.split('-')
            split_dot = split_dash[-1].split('.')
            args = {}
            args['ver1'] = split_dash[2]
            args['ver2'] = '.'.join([split_dot[0], split_dot[1]])
            args['arch'] = split_dot[2]
            args['name'] = old_ver
            url = base_url + URL_VER.format(**args)
            cmd = 'curl -O {}'.format(url)
            self.host.execute(cmd)
        # install old ver
        cmd = "rpm -i {}".format(old_ver)
        self.host.execute(cmd)
        # yum update to latest ver
        cmd = "yum update -y cockpit-machines"
        self.host.execute(cmd)
        cmd = 'rpm -qa | grep cockpit-machines --color=never'
        ret = self.host.execute(cmd, raise_exception=False)
        self.assertEqual(ret + '.rpm', self.new_ver)

    def test_start_cockpit(self):
        cmd = 'systemctl enable cockpit.socket && systemctl restart cockpit.socket'
        self.host.execute(cmd)
