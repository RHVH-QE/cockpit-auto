import time
from fabric.api import env, run, put
from fabric.network import disconnect_all
from constants import PROJECT_ROOT


RHEL_STRING = "10.73.75.57"
RHEL_USER = "root"
RHEL_PASSWORD = "redhat"
RHEL_REPO_FILE = "rhel74.repo"
RHV_REPO_RPM = "http://bob.eng.lab.tlv.redhat.com/builds/latest_4.2/rhv-release-latest-4.2.noarch.rpm"
YUM_UPDATE_TIMEOUT = 1200
YUM_INSTALL_TIMEOUT = 1200
ENTER_SYSTEM_MAXCOUNT = 10
ENTER_SYSTEM_INTERVAL = 60
ENTER_SYSTEM_TIMEOUT = 600


class Rhel(object):
    def __init__(self, host_string, host_user, host_passwd):
        self.host_string = host_string
        self.host_user = host_user
        self.host_pass = host_passwd
        self.set_env()

    def set_env(self):
        env.host_string = self.host_string
        env.user = self.host_user
        env.password = self.host_pass
        env.disable_known_hosts = True
        env.connection_attempts = 120

    def run_cmd(self, cmd, timeout=60):
        ret = None
        print "Run cmd '{}' on '{}'".format(cmd, self.host_string)
        try:
            ret = run(cmd, quiet=True, timeout=timeout)
            print ret
            if ret.succeeded:
                return True, ret
            else:
                return False, ret
        except Exception as e:
            return False, e

    def put_remote_file(self, local_path, remote_path):
        ret = put(local_path, remote_path)
        if not ret.succeeded:
            raise ValueError("Can't put {} to remote server:{}.".format(
                local_path, env.host_string))

    def _enter_system(self):

        cmd = "systemctl reboot"
        self.run_cmd(cmd, timeout=10)

        disconnect_all()

        count = 0
        while (count < ENTER_SYSTEM_MAXCOUNT):
            time.sleep(ENTER_SYSTEM_INTERVAL)
            ret = self.run_cmd(
                "cat /etc/os-release", timeout=ENTER_SYSTEM_TIMEOUT)
            if not ret[0]:
                count = count + 1
            else:
                break
        return ret

    def _setup_repo(self):
        local_path = "{0}/utils/static/{1}".format(
            PROJECT_ROOT, RHEL_REPO_FILE)
        remote_path = "/etc/yum.repos.d/{}".format(RHEL_REPO_FILE)
        try:
            self.put_remote_file(local_path, remote_path)
        except ValueError:
            return False
        return True

    def update_system(self):
        if not self._setup_repo():
            return False

        cmd = "yum update -y"
        ret = self.run_cmd(cmd, timeout=YUM_UPDATE_TIMEOUT)
        if not ret[0]:
            return False

        ret = self._enter_system()
        return ret[0]

    def _install_rhv_repo(self):
        cmd = "rpm -qa|grep rhv-release"
        ret = self.run_cmd(cmd)
        if ret[0]:
            cmd = "yum remove -y {}".format(ret[1])
            self.run_cmd(cmd)
        cmd = "yum install -y {}".format(RHV_REPO_RPM)
        self.run_cmd(cmd)

    def install_ovirt(self, package_url):
        self._install_rhv_repo()

        cmd = "rpm -q cockpit-ovirt-dashboard"
        ret = self.run_cmd(cmd)

        cmd = "yum update -y {}".format(package_url) if ret[0] else \
            "yum install -y {}".format(package_url)
        ret = self.run_cmd(cmd, timeout=YUM_INSTALL_TIMEOUT)
        if not ret[0]:
            return False

        cmd = "systemctl enable --now cockpit.socket"
        self.run_cmd(cmd)

        cmd = "firewall-cmd --add-service=cockpit"
        self.run_cmd(cmd)

        cmd = "firewall-cmd --add-service=cockpit --permanent"
        self.run_cmd(cmd)

        return True


RHEL = Rhel(RHEL_STRING, RHEL_USER, RHEL_PASSWORD)
