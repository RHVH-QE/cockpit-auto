import logging, re, simplejson
from cases.helpers import CheckBase


log = logging.getLogger('sherry')


class TestDashboardNodectl(CheckBase):

    def check_nodectl_help(self):
        """
        Purpose:
            Show nodectl help message in Terminal
        """
        log.info('Checking nodectl help...')

        cmd1 = 'nodectl -h'
        ret1 = self.run_cmd(cmd1)
        if ret1[0]:
            output1 = ret1[1]
        else:
            return False
        cmd2 = 'nodectl --help'
        ret2 = self.run_cmd(cmd2)
        if ret2[0]:
            output2 = ret2[1]
        else:
            return False

        cmd3 = 'nodectl'
        ret3 = self.run_cmd(cmd3)
        output3 = ret3[1]

        try:
            assert output1 == output2, 'nodectl help output not equal'
            assert output1 == output3, 'nodectl help output not equal'
            assert re.search('usage:', output1), 'nodectl help not correct'
            assert re.search('optional arguments:', output1), 'nodectl help not correct'
            assert re.search('Sub-commands:', output1), 'nodectl help not correct'
        except AssertionError as e:
            log.exception(e)
            return False

        return True

    def check_nodectl_version(self):
        """
        Purpose:
            Check nodectl version in Terminal
        """
        log.info('Checking nodectl version...')

        cmd1 = 'nodectl --version'
        ret1 = self.run_cmd(cmd1)
        if ret1[0]:
            output1 = ret1[1]
        else:
            return False

        cmd2 = 'rpm -q ovirt-node-ng-nodectl'
        ret2 = self.run_cmd(cmd2)
        if ret2[0]:
            output2 = ret2[1]
        else:
            return False

        try:
            output1 = output1.lstrip('nodectl-')
            output2 = output2.lstrip('ovirt-node-ng-nodectl-').split('-')[0]
            assert output1 == output2, 'nodectl verison not correct'
        except AssertionError as e:
            log.exception(e)
            return False

        return True

    def check_nodectl_info(self):
        """
        Purpose:
            Show information about the image in Terminal
        """
        log.info('Checking nodectl info...')

        cmd = 'nodectl info --machine-readable'
        ret = self.run_cmd(cmd)
        if ret[0]:
            output = ret[1]
        else:
            return False

        info_dict = simplejson.loads(output)

        try:
            layer = self.build
            assert 'layers' in info_dict.keys(), 'nodectl info not correct'
            assert layer in info_dict['layers'].keys(), 'nodectl info not correct'

            assert 'bootloader' in info_dict.keys(), 'nodectl info not correct'
            entry = layer + '+1'
            assert info_dict['bootloader']['default'] == entry, 'nodectl info not correct'
            assert 'current_layer' in info_dict.keys()
            assert entry == info_dict['current_layer'], 'nodectl info not correct'
        except AssertionError as e:
            log.exception(e)
            return False

        return True

    def check_nodectl_check(self):
        """
        Purpose:
            Check the system status in Terminal
        """
        log.info('Checking nodectl check...')
        cmd = 'nodectl check --machine-readable'
        ret = self.run_cmd(cmd)
        if ret[0]:
            output = ret[1]
        else:
            return False
        status_dict = simplejson.loads(output)
        nodectl_check_status = status_dict['status']
        mount_points_status = status_dict['mount_points']['status']
        basic_storage_status = status_dict['basic_storage']['status']
        vdsmd_status = status_dict['vdsmd']['status']
        cmd = 'systemctl status vdsmd.service|grep Active'
        ret = self.run_cmd(cmd)
        if ret[0]:
            output = ret[1]
        else:
            return False
        sys_vdsmd_status = output.split()[1]
        try:
            if sys_vdsmd_status == 'active':
                assert nodectl_check_status == 'ok', 'nodectl check status: bad'
                assert vdsmd_status == 'ok', 'nodectl check vdsmd: bad'
            else:
                assert mount_points_status == 'ok', 'nodectl check mount points: bad'
                assert basic_storage_status == 'ok', 'nodectl check basci storage: bad'
        except AssertionError as e:
            log.exception(e)
            return False

        return True

    def check_nodectl_json(self):
        """
        Purpose:
            Check the JSON output for nodectl in Terminal
        """
        log.info('Checking nodectl json...')

        cmd = 'nodectl info --machine-readable'
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False

        try:
            nodectl_info_dict = simplejson.loads(ret[1])
            assert nodectl_info_dict, 'nodectl json output failed'
        except AssertionError as e:
            log.exception(e)
            return False

        cmd = 'nodectl check --machine-readable'
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False
        try:
            nodectl_check_dict = simplejson.loads(ret[1])
            assert nodectl_check_dict, 'nodectl json output failed'
        except AssertionError as e:
            log.exception(e)
            return False

        return True

    def check_nodectl_motd(self):
        """
        Purpose:
            Check the motd for nodectl in Terminal
        """
        log.info('Checking nodectl motd...')

        cmd = 'nodectl motd'
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False
        output = ret[1]

        try:
            assert output, 'nodectl motd output failed'
        except AssertionError as e:
            log.error(e)
            return False

        return True

    def check_nodectl_banner(self):
        """
        Purpose:
            Check the generate-banner output for nodectl in Terminal
        """
        log.info('Checking nodectl banner...')
        cmd = 'nodectl generate-banner'
        ret = self.run_cmd(cmd)
        if ret[0]:
            output1 = ret[1]
        else:
            return False

        cmd = "echo 'cockpit-ovirt' >> /etc/issue"
        self.run_cmd(cmd)

        cmd = 'nodectl generate-banner --update-issue'
        self.run_cmd(cmd)

        cmd = 'cat /etc/issue'
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False
        output2 = ret[1]

        try:
            assert re.search(output1, output2), 'nodectl generate-banner failed'
            assert not re.search('cockpit-ovirt', output2), 'nodectl generate-banner failed'
        except AssertionError as e:
            log.error(e)
            return False

        return True

    def check_nodectl_debug(self):
        """
        Purpose:
            Check the debug information of nodectl sub_commands in Terminal
        """
        log.info('Checking nodectl debug...')

        cmd = 'nodectl info --debug'
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False

        cmd = 'nodectl check --debug'
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False

        cmd = 'nodectl motd --debug'
        ret = self.run_cmd(cmd)
        if not ret[0]:
            return False

    def go_check(self, file_name):
        cks = {}
        try:
            cks = self.run_cases(file_name)
        except Exception as e:
            log.exception(e)

        return cks
