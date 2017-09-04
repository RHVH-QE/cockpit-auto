import time
import re
from selenium import webdriver
from fabric.api import run, settings, put, local
import logging
import urllib2
from vncdotool import api
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.a_texts = []
        self.a_text_flag = False

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            self.a_text_flag = True
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)

    def handle_endtag(self, tag):
        if tag == "a":
            self.a_text_flag = False

    def handle_data(self, data):
        if self.a_text_flag:
            if data.startswith("rhvm-appliance"):
                self.a_texts.append(data)


def get_latest_rhvm_appliance(appliance_path):
    """
    Purpose:
        Get the latest rhvm appliance from appliance parent path
    """
    # Get the html page from appliance path
    req = urllib2.Request(appliance_path)
    response = urllib2.urlopen(req)
    rhvm_appliance_html = response.read()

    # Parse the html
    mp = MyHTMLParser()
    mp.feed(rhvm_appliance_html)
    mp.close()

    # Get the latest rhvm appliance url link
    mp.a_texts.sort()
    latest_rhvm_appliance_name = mp.a_texts[-1]

    latest_rhvm_appliance_link = None
    for link in mp.links:
        if re.search(latest_rhvm_appliance_name, link):
            latest_rhvm_appliance_link = link

    latest_rhvm_appliance = appliance_path + latest_rhvm_appliance_link

    return latest_rhvm_appliance


def download_auto_answer(auto_answer):
    with settings(warn_only=True):
        cmd = "curl -o /tmp/he_vm_run %s" % auto_answer
        res = local(cmd, capture=True)
    if res.failed:
        assert 0, "Failed to download the auto answer file"


def press_keys(seq, cli):
    """press keys sequence

    """
    for keys in seq:
        if len(keys) > 1:
            for k in keys:
                cli.keyPress(k)
                time.sleep(0.5)
        elif len(keys) == 1:
            cli.keyPress("shift-%s" % keys[0])
        else:
            logging.warning("Error at least should have one key")


class HandleVNCSetup:

    def __init__(self, host_ip, host_user, host_password, vnc_password='redhat'):
        self.host_ip = host_ip
        self.host_user = host_user
        self.host_password = host_password
        self.vnc_password = vnc_password
        self._set_vnc_pass()
        self.cli = api.connect(self.host_ip, password=self.vnc_password)

    def _set_vnc_pass(self):
        with settings(warn_only=True, host_string=self.host_user + '@' + self.host_ip, password=self.host_password):
            run('hosted-engine --add-console-password --password=%s' % self.vnc_password, quiet=True)

    def vnc_vm_login(self, vm_password):
        for k in 'root':
            self.cli.keyPress(k)
            time.sleep(0.1)
        self.cli.keyPress('enter')
        time.sleep(1)

        for k in vm_password:
            self.cli.keyPress(k)
            time.sleep(0.1)
        self.cli.keyPress('enter')
        time.sleep(1)


def he_install(host_dict, nfs_dict, install_dict, vm_dict):
    host_ip = host_dict['host_ip']
    host_user = host_dict['host_user']
    host_password = host_dict['host_password']
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
    root_uri = "https://" + host_ip + ":" + cockpit_port
    nfs_ip = nfs_dict['nfs_ip']
    nfs_password = nfs_dict['nfs_password']
    nfs_path = nfs_dict['nfs_path']

    rhvm_appliance_path = install_dict['rhvm_appliance_path']
    he_nic = install_dict['he_nic']

    vm_mac = vm_dict['vm_mac']
    vm_fqdn = vm_dict['vm_fqdn']
    vm_ip = vm_dict['vm_ip']
    vm_password = vm_dict['vm_password']
    engine_password = vm_dict['engine_password']
    auto_answer = vm_dict['auto_answer']


    # Delete the files in nfs storage path
    with settings(
        warn_only=True,
        host_string='root@' + nfs_ip,
        password=nfs_password):
        run("rm -rf %s/*" % nfs_path)
        run("service nfs restart", quiet=True)

    # Get the rhvm_appliance from rhvm_appliance_path
    rhvm_appliance_link = get_latest_rhvm_appliance(rhvm_appliance_path)
    local_rhvm_appliance = "/root/%s" % rhvm_appliance_link.split('/')[-1]
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd = "curl -o %s %s" % (local_rhvm_appliance, rhvm_appliance_link)
        output = run(cmd)
    if output.failed:
        raise RuntimeError("Failed to download the latest rhvm appliance")

    # Add host to /etc/hosts and install rhvm_appliance
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd0 = "hostname"
        host_name = run(cmd0)
        cmd1 = "echo '%s  %s' >> /etc/hosts" % (host_ip, host_name)
        run(cmd1)
        cmd2 = "echo '%s  %s' >> /etc/hosts" % (vm_ip, vm_fqdn)
        run(cmd2)
        cmd3 = "rpm -ivh %s" % local_rhvm_appliance
        run(cmd3)
        cmd4 = "rm -f %s" % local_rhvm_appliance
        run(cmd4)

    time.sleep(2)
    dr = webdriver.Chrome()
    dr.get(root_uri)
    time.sleep(5)
    id = dr.find_element_by_id
    class_name = dr.find_element_by_class_name
    tag_name = dr.find_elements_by_tag_name
    xpath = dr.find_element_by_xpath

    # Login to cockpit
    id("login-user-input").send_keys(host_user)
    time.sleep(2)
    id("login-password-input").send_keys(host_password)
    time.sleep(2)
    id("login-button").click()
    time.sleep(5)
    dr.get(root_uri + "/ovirt-dashboard")
    dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
    xpath("//a[@href='#/he']").click()
    time.sleep(5)

    class_name("btn-primary").click()    # Click to deploy HE
    time.sleep(10)
    class_name("btn-default").click()    # click next button,continue yes
    # dr.implicitly_wait(60)
    time.sleep(60)

    class_name("btn-default").click()    # specify storage mode
    time.sleep(2)

    nfs_storage = nfs_ip + ':' + nfs_path
    list(tag_name("input"))[0].send_keys(nfs_storage)  # NFS storage path
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(5)

    class_name("btn-default").click()    # iptables default confirm
    time.sleep(2)

    class_name("btn-default").click()    # gateway ip confirm
    time.sleep(2)

    list(tag_name("input"))[0].clear()   # select NIC
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(he_nic)
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()    # select appliance
    time.sleep(120)

    class_name("btn-default").click()    # select vnc
    time.sleep(2)

    class_name("btn-default").click()    # select cloud-init
    time.sleep(2)

    class_name("btn-default").click()    # select Generate
    time.sleep(2)

    list(tag_name("input"))[0].send_keys(vm_fqdn)  # set VM FQDN
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()       # set vm domain
    time.sleep(2)

    list(tag_name("input"))[0].clear()      # Manual setup
    time.sleep(2)
    list(tag_name("input"))[0].send_keys("No")
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    list(tag_name("input"))[0].clear()      # set root password
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(vm_password)
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)
    list(tag_name("input"))[0].clear()
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(vm_password)
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()     # leave ssh key empty
    time.sleep(2)

    list(tag_name("input"))[0].clear()    # enable ssh access for root
    time.sleep(2)
    list(tag_name("input"))[0].send_keys("yes")
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()     # set vm disk,default
    time.sleep(2)

    class_name("btn-default").click()     # set vm memory,default
    time.sleep(2)

    class_name("btn-default").click()     # set cpu type,default
    time.sleep(2)

    class_name("btn-default").click()     # set the number of vcpu
    time.sleep(2)

    list(tag_name("input"))[0].clear()    # set unicast MAC
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(vm_mac)
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()     # network,default DHCP
    time.sleep(2)

    class_name("btn-default").click()     # resolve hostname
    time.sleep(2)

    list(tag_name("input"))[0].clear()    # set engine admin password
    time.sleep(1)
    list(tag_name("input"))[0].send_keys(engine_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(1)
    list(tag_name("input"))[0].clear()
    time.sleep(1)
    list(tag_name("input"))[0].send_keys(engine_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()    # set the name of SMTP
    time.sleep(1)

    class_name("btn-default").click()    # set the port of SMTP,default 25
    time.sleep(1)

    class_name("btn-default").click()    # set email address
    time.sleep(1)

    class_name("btn-default").click()    # set comma-separated email address
    time.sleep(5)

    class_name("btn-default").click()    # confirm the configuration
    time.sleep(600)

    # Handle vnc to login, which is for engine-setup go script
    HandleVNCSetup(
        host_ip=host_ip,
        host_user=host_user,
        host_password=host_password).vnc_vm_login(vm_password)
    time.sleep(10)

    # Run engine-setup by go auto_answer script
    download_auto_answer(auto_answer)

    with settings(
        host_string='root@' + vm_ip,
        password=vm_password):
        put("/tmp/he_vm_run", "/root/run")
        run("chmod 755 /root/run")
        run("/root/run -i")
    time.sleep(60)

    class_name("btn-default").click()
    time.sleep(600)

    # Reboot the host
    with settings(
        host_string=host_user + '@' + host_ip,
        password=host_password):
        run("hosted-engine --vm-poweroff", quiet=True)
        time.sleep(30)
        run("hosted-engine --vm-start", quiet=True)
        time.sleep(120)

    dr.quit()


def check_he_is_deployed(host_ip, host_user, host_password):
    """
    Purpose:
        Check the HE is deployed on the host
    """
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd = "hosted-engine --check-deployed"
        ret = run(cmd)
        assert ret.succeeded, "HE is not deployed on %s" % host_ip

        cmd = "find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log"
        ret = run(cmd)
        assert ret.succeeded, "No hosted engine setup log found"

        cmd = "grep 'Hosted Engine successfully deployed' %s" % ret
        ret = run(cmd)
        assert ret.succeeded, "Not found the successfully message in the setup log %s" % ret
