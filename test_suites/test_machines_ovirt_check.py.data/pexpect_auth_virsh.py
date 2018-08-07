import pexpect
import sys

def get_auth_virsh_xml(user, passwd, cmd):
    child = pexpect.spawn(cmd)
    child.expect('Please enter your authentication name:')
    child.sendline(user)

    child.expect('Please enter your password:')
    child.sendline(passwd)
    child.read()
    return child.before

if __name__ == "__main__":
    cmd = sys.argv[1]
    print get_auth_virsh_xml("vdsm@ovirt", "shibboleth", cmd)
