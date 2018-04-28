from fabric.api import settings, run, get, put


class Machine(object):
    """"""

    def __init__(self, host_string, host_user, host_passwd):
        self.host_string = host_string
        self.host_user = host_user
        self.host_passwd = host_passwd

    def execute(self, cmd, timeout=60):
        ret = None
        try:
            with settings(
                    host_string=self.host_string,
                    user=self.host_user,
                    password=self.host_passwd,
                    disable_known_hosts=True,
                    connection_attempts=60):
                ret = run(cmd, quiet=True, timeout=timeout)
                if ret.succeeded:
                    return True, ret
                else:
                    return False, ret
        except Exception as e:
            return False, e

    def get_file(self, src_path, dst_path):
        ret = None
        try:
            with settings(
                    host_string=self.host_string,
                    user=self.host_user,
                    password=self.host_passwd,
                    disable_known_hosts=True,
                    connection_attempts=120):
                ret = get(src_path, dst_path)
                if ret.succeeded:
                    return True, ret
                else:
                    return False, ret
        except Exception as e:
            return False, e

    def put_file(self, src_path, dst_path):
        ret = None
        try:
            with settings(
                    host_string=self.host_string,
                    user=self.host_user,
                    password=self.host_passwd,
                    disable_known_hosts=True,
                    connection_attempts=120):
                ret = put(src_path, dst_path)
                if ret.succeeded:
                    return True, ret
                else:
                    return False, ret
        except Exception as e:
            return False, e
