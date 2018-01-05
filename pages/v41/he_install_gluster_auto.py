import time
import os
import re
import logging
from selenium import webdriver
from fabric.api import run, settings, put, local, get, env
import urllib2
from vncdotool import api
from HTMLParser import HTMLParser
from cases import CONF
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ConfigParser


log = logging.getLogger("sherry")



host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
    'host_password'), CONF.get('common').get('browser')

rhn_user, rhn_password = CONF.get('subscription').get('rhn_user'), CONF.get(
    'subscription').get('rhn_password')

gluster_ip, gluster_storage_path, rhvm_appliance_path, vm_mac, vm_fqdn, vm_ip, vm_password, engine_password, auto_answer = CONF.get(
    'hosted_engine'
).get('glusterfs_ip'), CONF.get('hosted_engine').get('gluster_storage_path'),CONF.get('hosted_engine').get(
    'rhvm_appliance_path'
), CONF.get('hosted_engine').get('he_vm_mac'), CONF.get('hosted_engine').get(
    'he_vm_fqdn'), CONF.get('hosted_engine').get('he_vm_ip'), CONF.get(
    'hosted_engine').get('he_vm_password'), CONF.get('hosted_engine').get('engine_password'), CONF.get('hosted_engine').get(
    'auto_answer')



env.host_string = host_user + '@' + host_ip
env.password = host_password

gluster_data_node1, gluster_data_node2, gluster_arbiter_node, vmstore_is_arbiter, data_is_arbiter, data_disk_count, device_name_engine, device_name_data, device_name_vmstore, size_of_datastore_lv, size_of_vmstore_lv, gdeploy_conf_file_path, mount_engine_brick, mount_data_brick, mount_vmstore_brick, gluster_vg_name, gluster_pv_name, number_of_Volumes, engine_lv_name = CONF.get(
    'gluster_details'
).get('gluster_data_node1'), CONF.get('gluster_details').get('gluster_data_node2'), CONF.get('gluster_details').get(
    'gluster_arbiter_node'), CONF.get('gluster_details').get('vmstore_is_arbiter'), CONF.get('gluster_details').get(
    'data_is_arbtier'), CONF.get('gluster_details').get('data_disk_count'), CONF.get('gluster_details').get(
    'device_name_engine'), CONF.get('gluster_details').get('device_name_data'), CONF.get('gluster_details').get(
    'device_name_vmstore'), CONF.get('gluster_details').get('size_of_datastore_lv'), CONF.get('gluster_details').get(
    'size_of_vmstore_lv'), CONF.get('gluster_details').get('gdeploy_conf_file_path'), CONF.get('gluster_details').get(
    'mount_engine_brick'), CONF.get('gluster_details').get('mount_data_brick'), CONF.get('gluster_details').get(
    'mount_vmstore_brick'), CONF.get('gluster_details').get('gluster_vg_name'), CONF.get('gluster_details').get(
    'gluster_pv_name'), CONF.get('gluster_details').get('number_of_Volumes'), CONF.get('gluster_details').get(
    'engine_lv_name')





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
    # log.info("Getting the latest rhvm appliance...")
    req = urllib2.Request(appliance_path)
    response = urllib2.urlopen(req)
    rhvm_appliance_html = response.read()
    # Parse the html
    mp = MyHTMLParser()
    mp.feed(rhvm_appliance_html)
    mp.close()

    # Get the latest rhvm appliance url link
    mp.a_texts.sort()
    link_42 = []
    # link_42 = []
    all_link = mp.a_texts
    for link in all_link:
        if "4.2" in link:
            link_42.append(link)

    latest_rhvm_appliance_name = link_42[-1]

    latest_rhvm_appliance_link = None
    for link in mp.links:
        if re.search(latest_rhvm_appliance_name, link):
            latest_rhvm_appliance_link = link

    latest_rhvm_appliance = appliance_path + latest_rhvm_appliance_link
    
    return latest_rhvm_appliance


def verify_gluster_deployment(host_dict):
    host_ip = host_dict['host_ip']
    host_user = host_dict['host_user']
    host_password = host_dict['host_password']
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        while(True):
            cmd0 = 'gluster volume list'
            ret0 = run(cmd0)
            if not ret0.__contains__("vmstore"):
                log.info("waiting for gluster deployment to finish")
            else:
                volume_list = ret0.split("\n")
                if volume_list.__len__() == number_of_Volumes:
                    cmd1 = "gluster volume info vmstore | grep Status" 
                    ret1 = run(cmd1)
                    if ret1.__contains__("Status: Started"):
                        time.sleep(10)
                        break
    

def he_install_gluster_auto(host_dict, gluster_storage_dict, install_dict, vm_dict, gluster_dict):
    host_ip = host_dict['host_ip']
    host_user = host_dict['host_user']
    host_password = host_dict['host_password']
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
    root_uri = "https://" + host_ip + ":" + cockpit_port
    gluster_ip = gluster_storage_dict['gluster_ip']
    gluster_storage_path = gluster_storage_dict['gluster_storage_path']

    rhvm_appliance_path = install_dict['rhvm_appliance_path']
    he_nic = install_dict['he_nic']

    vm_mac = vm_dict['vm_mac']
    vm_fqdn = vm_dict['vm_fqdn']
    vm_ip = vm_dict['vm_ip']
    vm_password = vm_dict['vm_password']
    engine_password = vm_dict['engine_password']
    auto_answer = vm_dict['auto_answer']

    # Subscription to RHSM via CMD
    log.info("Subscription to RHN or RHSM ,then enable rhvh repos...")
    for gluster_node_name, gluster_node_ip in gluster_dict.items():
        with settings(
            warn_only=True,
            host_string=host_user + '@' + gluster_node_ip,
            password=host_password):
            cmd0 = "subscription-manager register --username=%s --password=%s" % (
                rhn_user, rhn_password)
            run(cmd0)
            cmd1 = "subscription-manager attach --auto"
            run(cmd1)
            cmd2 = "subscription-manager repos --enable=rhel-7-server-rhvh-4-rpms"
            run(cmd2)
            cmd3 = "subscription-manager repos --list-enable |grep 'Repo ID' |grep 'rhvh'"
            output = run("os.popen(cmd3).read()")
            if output == 0:
                raise RuntimeError("Failed to find rhvh repos")

    
    #Downloading the rhevm appliance to the host machine
    rhvm_appliance_link = rhvm_appliance_path
    local_rhvm_appliance = "/root/%s" % rhvm_appliance_link.split('/')[-2]
    log.info("Getting the latest rhvm appliance...")
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd = "curl -o %s %s" % (local_rhvm_appliance, rhvm_appliance_link)
        output = run(cmd)
    if output.failed:
        raise RuntimeError("Failed to download the latest rhvm appliance")

    # Add host to /etc/hosts and install rhvm_appliance
    log.info(
        "Adding the host to /etc/hosts and installing the rhvm appliance...")
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd0 = "hostname"
        host_name = run(cmd0)
        cmd1 = "echo '%s  %s' >> /etc/hosts" % (host_ip, host_name)
        run(cmd1)
        cmd2 = "echo '%s' > /etc/hostname" % host_name
        run(cmd2)
        cmd3 = "hostname %s" % host_name
        run(cmd3)
        cmd4 = "echo '%s  %s' >> /etc/hosts" % (vm_ip, vm_fqdn)
        run(cmd4)
        cmd5 = "rpm -ivh %s" % local_rhvm_appliance
        run(cmd5)
        cmd6 = "rm -f %s" % local_rhvm_appliance
        run(cmd6)
    
    time.sleep(2)
    log.info("Deploying gluster...")
    dr = webdriver.Firefox()
    dr.get(root_uri)
    time.sleep(5)
    id = dr.find_element_by_id
    class_name = dr.find_element_by_class_name
    tag_name = dr.find_elements_by_tag_name
    xpath = dr.find_element_by_xpath
    xpaths = dr.find_elements_by_xpath
    

    # Login to cockpit
    log.info("Logining to the cockpit...")
    id("login-user-input").send_keys(host_user)
    time.sleep(2)
    id("login-password-input").send_keys(host_password)
    time.sleep(2)
    id("login-button").click()
    time.sleep(5)
    dr.get(root_uri + "/ovirt-dashboard")
    time.sleep(5)
    dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
    time.sleep(2)
    xpath("//a[@href='#/he']").click()
    time.sleep(5)

      

    # code for configuring gluster
    log.info("Configuring gluster to deploy Hosted Engine............")
    xpath("//input[@value='hci']").click()
    time.sleep(2)
    xpath("//button[@class='btn btn-lg btn-primary']").click()
    time.sleep(2)
    xpaths("//input[@placeholder='Gluster network address']")[0].send_keys(gluster_data_node1)
    time.sleep(2)
    xpaths("//input[@placeholder='Gluster network address']")[1].send_keys(gluster_data_node2)
    time.sleep(2)
    xpaths("//input[@placeholder='Gluster network address']")[2].send_keys(gluster_arbiter_node)
    time.sleep(2)
    xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
    time.sleep(2)
    xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
    time.sleep(2)
    xpaths("//input[@title='Third host in the host list will be used for creating arbiter bricks']")[1].click()
    time.sleep(2)
    xpaths("//input[@title='Third host in the host list will be used for creating arbiter bricks']")[2].click()
    time.sleep(2)
    xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
    xpaths("//input[@type='number']")[1].clear()
    time.sleep(1)
    xpaths("//input[@type='number']")[1].send_keys(data_disk_count)
    time.sleep(1)
    xpaths("//input[@placeholder='device name']")[0].clear()
    xpaths("//input[@placeholder='device name']")[0].send_keys(device_name_engine)
    time.sleep(1)
    xpaths("//input[@placeholder='device name']")[1].clear()
    xpaths("//input[@placeholder='device name']")[1].send_keys(device_name_data)
    time.sleep(1)
    xpaths("//input[@placeholder='device name']")[2].clear()
    xpaths("//input[@placeholder='device name']")[2].send_keys(device_name_vmstore)
    time.sleep(1)
    xpaths("//input[@type='number']")[3].clear()
    time.sleep(1)
    xpaths("//input[@type='number']")[3].send_keys(size_of_datastore_lv)
    time.sleep(1)
    xpaths("//input[@type='number']")[4].clear()
    time.sleep(1)
    xpaths("//input[@type='number']")[4].send_keys(size_of_vmstore_lv)
    time.sleep(1)
    xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
    time.sleep(5)
    xpath("//button[@class='btn btn-primary wizard-pf-finish']").click()
    verify_gluster_deployment(host_dict)
    time.sleep(10)
    if not xpath("//button[@class='btn btn-lg btn-primary']").is_displayed():
        log.error("continue to Hosted Engine deployment not found")
        
    else:
        log.info("Going to Deploy HostedEngine on Gluster...")
    
    # Test starts from here
    xpath("//button[@class='btn btn-lg btn-primary']").click() # click on button 'Continue to Hosted Engine deployment'
    time.sleep(10)
    class_name("btn-default").click()  # click next button,continue yes
    time.sleep(20)
    list(tag_name("input"))[0].clear()  # clear the text box to configure gluster cluster
    time.sleep(5)
    list(tag_name("input"))[0].send_keys("Yes") #entering the input as yes to configure gluster cluster
    time.sleep(5)
    class_name("btn-default").click()  # click next button, continue yes
    time.sleep(10)
    
    class_name("btn-default").click()  # gateway ip confirm
    time.sleep(5)

    list(tag_name("input"))[0].clear()  # select NIC
    time.sleep(5)
    list(tag_name("input"))[0].send_keys(he_nic)
    time.sleep(5)

    class_name("btn-default").click() #confirm nic  
    time.sleep(5)

    class_name("btn-default").click() #select the appliance
    time.sleep(120)

    class_name("btn-default").click()  # select vnc
    time.sleep(2)

    class_name("btn-default").click()  # select cloud-init
    time.sleep(2)

    list(tag_name("input"))[0].send_keys(vm_fqdn)  # set VM FQDN
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()  # set vm domain
    time.sleep(2)

    class_name("btn-default").click() #Automatically setup engine-setup on first boot
    time.sleep(2)

    list(tag_name("input"))[0].clear()  # Enter root password that will be used for engine appliance
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(vm_password)
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)
    list(tag_name("input"))[0].clear()
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(vm_password) #confirm appliance password
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()  # leave ssh key empty
    time.sleep(2)

    list(tag_name("input"))[0].clear()  # enable ssh access for root
    time.sleep(2)
    list(tag_name("input"))[0].send_keys("yes")
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()  # set vm disk size,default
    time.sleep(2)

    class_name("btn-default").click()  # set vm memory,default
    time.sleep(2)

    class_name("btn-default").click()  # set cpu type,default
    time.sleep(2)

    class_name("btn-default").click()  # set the number of vcpu
    time.sleep(2)

    list(tag_name("input"))[0].clear()  # set unicast MAC
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(vm_mac)
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()  # network,default DHCP
    time.sleep(2)

    class_name("btn-default").click()  # resolve hostname
    time.sleep(2)

    list(tag_name("input"))[0].clear()  # set engine admin password
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(engine_password)
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)
    list(tag_name("input"))[0].clear()
    time.sleep(2)
    list(tag_name("input"))[0].send_keys(engine_password) #confirm the engine password again
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)

    class_name("btn-default").click()  # set the name of SMTP
    time.sleep(2)

    class_name("btn-default").click()  # set the port of SMTP,default 25
    time.sleep(2)

    class_name("btn-default").click()  # set email address
    time.sleep(2)

    class_name("btn-default").click()  # set comma-separated email address
    time.sleep(5)

    class_name("btn-default").click()  # confirm the configuration
    
    


def check_he_is_deployed(host_ip, host_user, host_password):
    """
    Purpose:
        Check the HE is deployed on the host
    """
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        
        while (True):
            cmd = "hosted-engine --vm-status | grep 'Engine status'"
            ret = run(cmd)
            if not ret.__contains__('"health": "good", "vm": "up"'):
                log.info("Waiting for HE to be deployed on host %s" % host_ip)
            else:
                log.info ("HE is deployed on %s" % host_ip)
                break
            

        cmd = "find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log"
        ret = run(cmd)
        if ret.succeeded == True:
            log.info("Hosted engine setup log found")
        else:
            log.error("No hosted engine log found")
        
        cmd = "grep 'Hosted Engine successfully deployed' %s" % ret
        ret = run(cmd)
        if ret.succeeded == True:
            log.info("Found the successfully message in the setup log %s" % ret)
        else:
            log.error("Not found the successfully message in the setup log %s" % ret)
                               
