from fabric.api import settings, run, get, put


class RunCmdError(Exception):
    pass


class Machine(object):
    """"""

    def __init__(self, host_string, host_user, host_passwd):
        self.host_string = host_string
        self.host_user = host_user
        self.host_passwd = host_passwd

    def execute(self, cmd, timeout=60):
        with settings(
                host_string=self.host_string,
                user=self.host_user,
                password=self.host_passwd,
                disable_known_hosts=True,
                connection_attempts=60):
            ret = run(cmd, quiet=True, timeout=timeout)
            if ret.succeeded:
                return ret
            else:
                raise RunCmdError("ERR: Run `{}` failed on host".format(cmd))

    def get_file(self, src_path, dst_path):
        with settings(
                host_string=self.host_string,
                user=self.host_user,
                password=self.host_passwd,
                disable_known_hosts=True,
                connection_attempts=120):
            ret = get(src_path, dst_path)
            if not ret.succeeded:
                raise RunCmdError(
                    "ERR: Get file {} to {} failed".format(src_path, dst_path))

    def put_file(self, src_path, dst_path):
        with settings(
                host_string=self.host_string,
                user=self.host_user,
                password=self.host_passwd,
                disable_known_hosts=True,
                connection_attempts=120):
            ret = put(src_path, dst_path)
            if not ret.succeeded:
                raise RunCmdError(
                    "ERR: Put file {} to {} failed".format(src_path, dst_path))
