from selenium import webdriver
from fabric.api import env, run, settings
from cases import CONF
from pages.v41.he_install_gluster_auto import *
from collections import OrderedDict
from utils.helpers import checkpoint1
import logging
import const

log = logging.getLogger("sherry")

dict1 = OrderedDict(zip(const.deployment_cases_RHHI, const.deployment_cases_RHHI_id))

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')

gluster_ip, gluster_storage_path, rhvm_appliance_path, vm_mac, vm_fqdn, vm_ip, vm_password, engine_password, auto_answer = CONF.get(
    'hosted_engine'
).get('gluster_ip'), CONF.get(
    'hosted_engine'
).get('gluster_engine_volume'), CONF.get('hosted_engine').get(
    'rhvm_appliance_path'
), CONF.get('hosted_engine').get('he_vm_mac'), CONF.get('hosted_engine').get(
    'he_vm_fqdn'), CONF.get('hosted_engine').get('he_vm_ip'), CONF.get(
        'hosted_engine').get('he_vm_password'), CONF.get('hosted_engine').get(
            'engine_password'), CONF.get('hosted_engine').get('auto_answer')

gluster_data_node1, gluster_data_node2, gluster_arbiter_node, vmstore_is_arbiter, data_is_arbiter, data_disk_count, device_name_engine, device_name_data, device_name_vmstore, size_of_datastore_lv, size_of_vmstore_lv, gdeploy_conf_file_path, mount_engine_brick, mount_data_brick, mount_vmstore_brick, gluster_vg_name, gluster_pv_name, number_of_Volumes, engine_lv_name, os_variant_rhvh = CONF.get(
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
    'engine_lv_name'), CONF.get('gluster_details').get('os_variant_rhvh')


env.host_string = host_user + '@' + host_ip
env.password = host_password


def init_browser():
    if browser == 'firefox':
        driver = webdriver.Firefox()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
    elif browser == 'chrome':
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
    else:
        raise NotImplementedError


@checkpoint1(dict1)
def check_engine_lv_of_type_thick_and_volume_of_type_replicate():
    """
    Purpose:
        RHHI-138
        check if engine lv is of type thick and volume is of type replicate
    """
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd0 = "lvs -o segtype %s" % engine_lv_name
        ret0 = run(cmd0)
        if ret0.__contains__("linear"):
            log.info("Engine lv is of type thick")
        else:
            log.error("Engine lv is not of type thick")
        cmd1 = "lvs -o lv_size %s" % engine_lv_name
        ret1 = run(cmd1)
        if ret1.__contains__("100.00g"):
            log.info("Engine lv size is 100GB")
        else:
            log.error("could not find Engine lv size")
        cmd2 = "gluster volume list"
        ret2 = run(cmd2)
        if ret2.__contains__("engine"):
            cmd3 = "gluster volume info engine | grep 'Number of Bricks'"
            ret3 = run(cmd3)
            ret3 = ret3.split(":")
            cmd4 = "gluster volume info engine | grep Type"
            ret4 = run(cmd4)
            ret4 = ret4.split(":")
            if ret3[1].lstrip() == "1 x 3 = 3" and ret4[1].lstrip() == "Replicate":
                log.info("Engine volume is of type Replicate")
            else:
                log.error("Engine volume is not of type replicate")
        else:
            log.error("No volume with name engine")
            
@checkpoint1(dict1)
def check_gluster_packages_presence_on_rhvh_node():
    """
       Purpose:
           RHHI-118
           check if gluster packages are present on RHV-H node
       """
    gluster_dict = {'gluster_data_node1': gluster_data_node1,
                    'gluster_data_node2': gluster_data_node2,
                    'gluster_arbiter_node': gluster_arbiter_node
                    }
    for gluster_node_name, gluster_node_ip in gluster_dict.items():
        with settings(
            warn_only=True,
            host_string=host_user + '@' + gluster_node_ip,
            password=host_password):
            cmd = 'rpm -qa | grep glusterfs'
            ret = run(cmd)
            if ret.succeeded == True:
                log.info("Following gluster packages are present on host %s %s" % (gluster_node_ip, ret))
            else:
                log.error("gluster packages are not present on host %s %s" % (gluster_node_ip, ret))
            cmd1 = 'rpm -qa | grep vdsm-gluster'
            ret1 = run(cmd1)
            if ret1.succeeded == True:
                log.info("vdsm-gluster package is present on host %s %s" % (gluster_node_ip, ret1))
            else:
                log.error("vdsm-gluster package is not present on host %s %s" % (gluster_node_ip, ret1))
                
                
@checkpoint1(dict1)
def check_glusterfs_firewall_service_availability_with_default_firewallzone():
    """
        Purpose:
            RHHI-119
            check glusterfs firewall service availabliity 
    """
    gluster_dict = {'gluster_data_node1': gluster_data_node1,
                    'gluster_data_node2': gluster_data_node2,
                    'gluster_arbiter_node': gluster_arbiter_node
                    }
    for gluster_node_name, gluster_node_ip in gluster_dict.items():
        with settings(
            warn_only=True,
            host_string=host_user + '@' + gluster_node_ip,
            password=host_password):
            cmd = 'firewall-cmd --list-services'
            ret = run(cmd)
            if ret.succeeded == True and ret.__contains__('glusterfs'):
                log.info("glusterfs firewall service is enabled by default on host %s, %s" % (gluster_node_ip, ret))
            else:
                log.error("glusterfs firewall service is not enabled by default on host %s, %s" % (gluster_node_ip, ret))
                
                
@checkpoint1(dict1)
def check_cockpitui_should_be_reachable_for_the_user():
    """
        Purpose:
            RHHI-121
            check cockpit ui should be reachable by the user
    """
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                 'host_password': host_password
                 }
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
    root_uri = "https://" + host_ip + ":" + cockpit_port
    dr = webdriver.Firefox()
    dr.get(root_uri)
    time.sleep(5)
    ret = dr.find_element_by_id('brand').text
    if ret.__contains__("RED HAT VIRTUALIZATION HOST 4.1 (EL7.4)"):
        log.info("cockpit page is available for host %s" % host_ip)
    else:
        log.error("cockpit page is not available for host %s " % host_ip)
    dr.quit()

@checkpoint1(dict1)
def check_option_to_start_with_gluster_deployment():
    """
        Purpose:
            RHHI-122
            check for gluster deployment option
    """
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                 'host_password': host_password
                 }
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
        root_uri = "https://" + host_ip + ":" + cockpit_port
        dr = webdriver.Firefox()
        dr.get(root_uri)
        time.sleep(5)
        # Login to cockpit
        log.info("Logging to the cockpit...")
        dr.find_element_by_id("login-user-input").send_keys(host_user)
        time.sleep(2)
        dr.find_element_by_id("login-password-input").send_keys(host_password)
        time.sleep(2)
        dr.find_element_by_id("login-button").click()
        time.sleep(5)
        dr.get(root_uri + "/ovirt-dashboard")
        time.sleep(5)
        dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
        time.sleep(5)
        dr.find_element_by_xpath("//a[@href='#/he']").click()
        time.sleep(5)
        # verify for gluster deploy button
        log.info("verify for gluster deploy button............")
        ret = dr.find_element_by_xpath("//input[@value='hci']").is_enabled()
        if ret == True:
            log.info("Gluster deploy button is enabled on %s" % (host_ip))
        else:
            log.error("glusterfs deploy button is not enabled or present %s " % (host_ip))
    dr.quit()

@checkpoint1(dict1)
def check_saving_the_generated_gdeploy_config_file():
    """
        Purpose:
            RHHI-127
            verify that generated gdeploy conf file is saved
    """
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd0 = "ls -l %s" % (gdeploy_conf_file_path)
        ret = run(cmd0)
        print ret
        if ret.__contains__(gdeploy_conf_file_path):
            log.info ("generated gdeploy conf file is saved at %s") % gdeploy_conf_file_path
        else:
            log.error("generated gdeploy conf file is not saved")

@checkpoint1(dict1)
def check_cockpit_gdeploy_plugin_provides_redeploy_button():
    """
        Purpose:
            RHHI-129
            verify that redeploy button exists if something fails
    """
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                 'host_password': host_password
                 }
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
        root_uri = "https://" + host_ip + ":" + cockpit_port
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
        time.sleep(5)
        xpath("//a[@href='#/he']").click()
        time.sleep(5)
        # code for configuring gluster
        log.info("Deploying the Hosted Engine setup by step............")
        xpath("//input[@value='hci']").click()
        time.sleep(2)
        xpath("//button[@class='btn btn-lg btn-primary']").click()
        time.sleep(2)
        xpaths("//input[@placeholder='Gluster network address']")[0].send_keys(host_ip)
        time.sleep(2)
        xpaths("//input[@placeholder='Gluster network address']")[1].send_keys(gluster_data_node2)
        time.sleep(2)
        xpaths("//input[@placeholder='Gluster network address']")[2].send_keys(gluster_arbiter_node)
        time.sleep(2)
        xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
        time.sleep(2)
        xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
        time.sleep(2)
        xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
        time.sleep(1)
        xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
        time.sleep(5)
        xpath("//button[@class='btn btn-primary wizard-pf-finish']").click()
        time.sleep(10)
        if xpath("//span[@class='pficon pficon-restart']").is_displayed():
            print xpath("//span[@class='pficon pficon-restart']")
            log.info("Redeploy button exists")
        else:
            log.error("Redeploy button does not exist")
    dr.quit()
        
        
@checkpoint1(dict1)
def check_cleanup_of_gluster_setup_done():
    """
        Purpose:
            RHHI-129
            verify that redeploy button exists if something fails
    """
    gluster_dict = {'gluster_data_node1': gluster_data_node1,
                    'gluster_data_node2': gluster_data_node2,
                    'gluster_arbiter_node': gluster_arbiter_node
                    }
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd0 = "gluster volume list"
        ret = run(cmd0)
        if ret.__contains__("No volumes present in the cluster"):
            log.info("No volumes present in the cluster")
        elif ret.__contains__("data"):
            volume_list = ret.split("\n")
            for volume in volume_list:
                volume = volume.rstrip()
                cmd1 = "gluster volume stop %s force --mode=script" % volume
                run(cmd1)
                cmd2 = "gluster volume info %s | grep Status" % volume
                ret = run(cmd2)
                if ret.__contains__("Status: Stopped"):
                    log.info("volume %s has been stopped successfully" % volume)
                    cmd3 = "gluster volume delete %s --mode=script" % volume
                    ret1 = run(cmd3)
                    if ret1.__contains__("success"):
                        log.info("Successfully deleted the volume %s" % volume)
                    else:
                        log.error("Could not delete volume %s" % volume)
                else:log.error("Volume %s could not be stopped" % volume)
                
        else:
            log.info("No volumes present")
        for gluster_node_name, gluster_node_ip in gluster_dict.items():
            cmd = "gluster peer detach %s" % gluster_node_ip
            ret = run(cmd)
            if ret == 0 or ret.__contains__("peer detach: success"):
                log.info("Successfully detached peers %s", gluster_node_ip)
            elif ret != 0 or ret.__contains__("peer detach: failed: %s is not part of cluster" % gluster_node_ip):
                log.info("peer %s not part of cluster", gluster_node_ip)
            else:
                log.error("Failed to peer detach the node '%s'.", gluster_node_ip)
            with settings(
                warn_only=True,
                host_string=host_user + '@' + gluster_node_ip,
                password=host_password):
                cmd = 'umount %s' % mount_engine_brick
                ret = run(cmd)
                if ret.__contains__("umount: %s: mountpoint not found" % mount_engine_brick):
                    log.error("Mount point not found %s", mount_engine_brick)
                else:
                    log.info("Umount done successfully %s", mount_engine_brick)
                cmd1 = 'umount %s' % mount_data_brick
                ret1 = run(cmd1)
                if ret.__contains__("umount: %s: mountpoint not found" % mount_data_brick):
                    log.error("Mount point not found %s", mount_data_brick)
                else:
                    log.info("Umount done successfully %s", mount_data_brick)
                cmd2 = 'umount %s' % mount_vmstore_brick
                ret2 = run(cmd2)
                if ret2.__contains__("umount: %s: mountpoint not found" % mount_vmstore_brick):
                    log.error("Mount point not found %s", mount_vmstore_brick)
                else:
                    log.info("Umount done successfully %s", mount_vmstore_brick)
                cmd3 = "rm -rf %s" % mount_engine_brick
                ret3 = run(cmd3)
                cmd4 = "rm -rf %s" % mount_data_brick
                ret4 = run(cmd4)
                cmd5 = "rm -rf %s" % mount_vmstore_brick
                ret5 = run(cmd5)
                cmd6 = "rm -rf /gluster_bricks"
                ret6 = run(cmd6)
                cmd7 = 'vgremove %s force -y' % gluster_vg_name
                ret7 = run(cmd7)
                if ret7 != 0 and ret7.__contains__("Volume group " '"%s"' " not found" % gluster_vg_name):
                    log.error("Volume group " '"%s"' "not found" % gluster_vg_name)
                else:
                    log.info("Volume group " '"%s"' "has been removed successfully" % gluster_vg_name)
                cmd8 = 'pvremove %s' % gluster_pv_name
                ret8 = run(cmd8)
                if ret8.__contains__("No PV label found on %s" % gluster_pv_name):
                    log.info("No PV label has been found")
                elif ret8.__contains__("Labels on physical volume " '"%s"' " successfully wiped" % gluster_pv_name):
                    log.info("Successfully wiped labels on physical volume %s", gluster_pv_name)
                else:
                    log.error("could not remove labels from pv")


@checkpoint1(dict1)
def check_deployment_with_hostedengine_on_gluster():
    """
        Purpose:
            RHHI-131 & 132
            verify that hosted engine deployment is done on gluster and gluster deployment is done.....
    """
    cmd = "ip a s|grep %s" % host_ip
    output = run(cmd)
    he_nic = output.split()[-1]
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                 'host_password': host_password
                 }

    gluster_dict = {'gluster_data_node1': gluster_data_node1,
                    'gluster_data_node2': gluster_data_node2,
                    'gluster_arbiter_node': gluster_arbiter_node
                    }

    gluster_storage_dict = {'gluster_ip': gluster_ip,
                            'gluster_storage_path': gluster_storage_path
                            }

    install_dict = {'rhvm_appliance_path': rhvm_appliance_path,
                    'he_nic': he_nic
                    }

    vm_dict = {
        'vm_mac': vm_mac,
        'vm_fqdn': vm_fqdn,
        'vm_ip': vm_ip,
        'vm_password': vm_password,
        'engine_password': engine_password,
        'auto_answer': auto_answer,
    }
    he_install_gluster_auto(host_dict, gluster_storage_dict, install_dict, vm_dict, gluster_dict)
    check_he_is_deployed(host_ip, host_user, host_password)
    log.info("HostedEngine was deployed!")

@checkpoint1(dict1)    
def check_gluster_deployment_wizard():
    """
        Purpose:
            RHHI-144
            check for gluster deployment wizard
    """
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                 'host_password': host_password
                 }
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
        root_uri = "https://" + host_ip + ":" + cockpit_port
        dr = webdriver.Firefox()
        dr.get(root_uri)
        time.sleep(5)
        # Login to cockpit
        log.info("Logging to the cockpit...")
        dr.find_element_by_id("login-user-input").send_keys(host_user)
        time.sleep(2)
        dr.find_element_by_id("login-password-input").send_keys(host_password)
        time.sleep(2)
        dr.find_element_by_id("login-button").click()
        time.sleep(5)
        dr.get(root_uri + "/ovirt-dashboard")
        time.sleep(5)
        dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
        time.sleep(5)
        dr.find_element_by_xpath("//a[@href='#/he']").click()
        time.sleep(5)
        # verify for gluster deployment Wizard
        dr.find_element_by_xpath("//input[@value='hci']").click()
        time.sleep(5)
        dr.find_element_by_xpath("//button[@class='btn btn-lg btn-primary']").click()
        time.sleep(5)
        if dr.find_element_by_xpath("//dt[@class='modal-title']").text == "Gluster Deployment":
            log.info ("Gluster deployment Wizard is present")
            dr.save_screenshot('screenshots/gluster_deployment_wizard.png')
        else:
            log.error("gluster deployment wizard is not present on host %s " % (host_ip))
            dr.save_screenshot('screenshots/gluster_deploymentwizard_not_present.png')
    dr.quit()

@checkpoint1(dict1)
def validate_host_deployment_tab():
    """
        Purpose:
            RHHI-145
            validate host deployment tab
    """
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                 'host_password': host_password
                 }
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
        root_uri = "https://" + host_ip + ":" + cockpit_port
        dr = webdriver.Firefox()
        dr.get(root_uri)
        time.sleep(5)
        # Login to cockpit
        log.info("Logging to the cockpit...")
        dr.find_element_by_id("login-user-input").send_keys(host_user)
        time.sleep(2)
        dr.find_element_by_id("login-password-input").send_keys(host_password)
        time.sleep(2)
        dr.find_element_by_id("login-button").click()
        time.sleep(5)
        dr.get(root_uri + "/ovirt-dashboard")
        time.sleep(5)
        dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
        time.sleep(5)
        dr.find_element_by_xpath("//a[@href='#/he']").click()
        time.sleep(5)
        # verify for gluster deployment Wizard
        dr.find_element_by_xpath("//input[@value='hci']").click()
        time.sleep(5)
        dr.find_element_by_xpath("//button[@class='btn btn-lg btn-primary']").click()
        time.sleep(5)
        log.info("validating for a hint for the user to enter gluster network address in the host text box")
        ret0 = dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[0].get_property("title")
        ret1 = dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[1].get_property("title")
        ret2 = dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[2].get_property("title")
        if ret0 and ret1 and ret2 == "Enter the address of gluster network which will be used for gluster data traffic.":
            log.info("Hint for the user is present to use gluster network as backend network IP for hosts")
        else:
            log.error("Hint is not present for the user to use gluster network as bakend network IP for hosts")
            dr.save_screenshot('screenshots/no_hint_present_gluster_network.png')
        dr.find_element_by_xpath("//a[@tabindex='0']").click()
        time.sleep(2)
        log.info("validating for a hint for the user on which host will be used as arbiter node")
        if dr.find_element_by_xpath("//div[@role='tooltip']").text == "This host will be used as arbiter node while creating arbiter volumes":
            log.info("Host text box hints the user about the host that will be used as arbiter node")
            dr.save_screenshot('screenshots/hint_for_arbiter_node.png')
        else:
            log.error("No hint for the user about arbiter node")
            dr.save_screenshot('screenshots/hint_for_no_arbiter_node.png')
        log.info("validating if host ips entered in the text boxs are retained")
        dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[0].send_keys(gluster_data_node1)
        time.sleep(5)
        ret3 = dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[0].get_property("value")
        if ret3 == gluster_data_node1:
            log.info("Value is retained in the host textbox")
        else:
            log.error("Value is not retained in the host textbox")
    dr.quit()

@checkpoint1(dict1)
def check_back_and_cancel_buttons_on_gdeploy_wizard():
    """
        Purpose:
            RHHI-148
            check back and cancel buttons on gdeploy wizard
    """
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                'host_password': host_password
                 }
    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
        root_uri = "https://" + host_ip + ":" + cockpit_port
        dr = webdriver.Firefox()
        dr.get(root_uri)
        time.sleep(5)
        # Login to cockpit
        log.info("Logging to the cockpit...")
        dr.find_element_by_id("login-user-input").send_keys(host_user)
        time.sleep(2)
        dr.find_element_by_id("login-password-input").send_keys(host_password)
        time.sleep(2)
        dr.find_element_by_id("login-button").click()
        time.sleep(5)
        dr.get(root_uri + "/ovirt-dashboard")
        time.sleep(5)
        dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
        time.sleep(5)
        dr.find_element_by_xpath("//a[@href='#/he']").click()
        time.sleep(5)
        # verify for gluster deployment Wizard
        dr.find_element_by_xpath("//input[@value='hci']").click()
        time.sleep(5)
        dr.find_element_by_xpath("//button[@class='btn btn-lg btn-primary']").click()
        time.sleep(5)
        if dr.find_element_by_xpath("//dt[@class='modal-title']").text == "Gluster Deployment":
            log.info("Gluster deployment Wizard is present and checking the functionality of back button")
            dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[0].send_keys(gluster_data_node1)
            time.sleep(2)
            dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[1].send_keys(gluster_data_node2)
            time.sleep(2)
            dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[2].send_keys(gluster_arbiter_node)
            time.sleep(2)
            dr.find_element_by_xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
            time.sleep(2)
            dr.find_element_by_xpath("//button[@class='btn btn-default wizard-pf-back']").click()
            time.sleep(2)
            if dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[0].is_displayed():
                log.info("Back button functions correctly in gluster deployment wizard")
            else:
                log.error("Back button does not function correctly in gluster deployment wizard")
                dr.save_screenshot('screenshots/back_button_gluster_deployment_wizard.png')
            dr.find_element_by_xpath("//button[@class='btn btn-default btn-cancel wizard-pf-cancel wizard-pf-dismiss']").click()
            time.sleep(5)
            if dr.find_element_by_xpath("//input[@value='hci']").is_displayed():
                log.info("Cancel button functions correctly in gluster deployment wizard")
            else:
                log.error("Cancel button does not function correctly in gluster deployment wizard")
                dr.save_screenshot('screenshots/cancel_button_gluster_deployment_wizard.png')
        else:
            log.error("gluster deployment wizard is not present on host %s " % host_ip)
            dr.save_screenshot('screenshots/gluster_deploymentwizard_not_present.png')
    dr.quit()
    
@checkpoint1(dict1)
def validate_arbiter_volume_creation():
    """
        Purpose:
            RHHI-147
            validate arbiter volume creation
    """
    with settings(
        warn_only=True,
        host_string=host_user + '@' + host_ip,
        password=host_password):
        cmd0 = "gluster volume list"
        ret0 = run(cmd0)
        volume_list = ret0.split("\n")
        for volume in volume_list:
            volume = volume.rstrip()
            if volume == "vmstore":
                cmd1 = "gluster volume info %s | grep 'Number of Bricks'" %volume
                ret1 = run(cmd1)
                ret1 = ret1.split(":")
                cmd2 = "gluster volume info %s | grep Type" %volume
                ret2 = run(cmd2)
                ret2 = ret2.split(":")
                if ret1[1].lstrip() == "1 x (2 + 1) = 3" and ret2[1].lstrip() == "Replicate":
                    log.info("volume %s has been created as arbiter volume" %volume)
                else:
                    log.error("volume %s has not been created as arbiter volume" %volume)
            if volume == "data":
                cmd1 = "gluster volume info %s | grep 'Number of Bricks'" % volume
                ret1 = run(cmd1)
                ret1 = ret1.split(":")
                cmd2 = "gluster volume info %s | grep Type" % volume
                ret2 = run(cmd2)
                ret2 = ret2.split(":")
                if ret1[1].lstrip() == "1 x (2 + 1) = 3" and ret2[1].lstrip() == "Replicate":
                    log.info("volume %s has been created as arbiter volume" % volume)
                else:
                    log.error("volume %s has not been created as arbiter volume" % volume)

@checkpoint1(dict1)
def validate_packages_tab():
    """
        Purpose:
            RHHI-146
            validate packages tab
    """
    host_dict = {'host_ip': host_ip,
                 'host_user': host_user,
                 'host_password': host_password
                 }


    if 'cockpit_port' in host_dict:
        cockpit_port = host_dict['cockpit_port']
    else:
        cockpit_port = "9090"
        root_uri = "https://" + host_ip + ":" + cockpit_port
        dr = webdriver.Firefox()
        dr.get(root_uri)
        time.sleep(5)
        # Login to cockpit
        log.info("Logging to the cockpit...")
        dr.find_element_by_id("login-user-input").send_keys(host_user)
        time.sleep(2)
        dr.find_element_by_id("login-password-input").send_keys(host_password)
        time.sleep(2)
        dr.find_element_by_id("login-button").click()
        time.sleep(5)
        dr.get(root_uri + "/ovirt-dashboard")
        time.sleep(5)
        dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
        time.sleep(5)
        dr.find_element_by_xpath("//a[@href='#/he']").click()
        time.sleep(5)
        # verify for gluster deployment Wizard
        dr.find_element_by_xpath("//input[@value='hci']").click()
        time.sleep(5)
        dr.find_element_by_xpath("//button[@class='btn btn-lg btn-primary']").click()
        time.sleep(5)
        dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[0].send_keys(
            gluster_data_node1)
        time.sleep(2)
        dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[1].send_keys(
        gluster_data_node2)
        time.sleep(2)
        dr.find_elements_by_xpath("//input[@placeholder='Gluster network address']")[2].send_keys(
        gluster_arbiter_node)
        time.sleep(2)
        dr.find_element_by_xpath("//button[@class='btn btn-primary wizard-pf-next']").click()
        time.sleep(2)
        with settings(
            warn_only=True,
            host_string=host_user + '@' + host_ip,
            password=host_password):
            cmd0 = "cat /etc/os-release"
            ret0 = run(cmd0)
            releases = ret0.split("\n")
            releases_list = []
            for values in releases:
                value = values.rstrip()
                releases_list.append(value)
            if os_variant_rhvh in releases_list:
                log.info ("os vairant is %s" % os_variant_rhvh)
                elements = dr.find_elements_by_xpath("//label[@class='col-md-2 control-label']")
                labels_list = []
                for labels in elements:
                    label = labels.text
                    labels_list.append(label)
                
                if "Repositories" in labels_list:
                    log.info("Repositories textbox is present in pacakges tab of Gluster Wizard")
                else:
                    log.error("Repositories textbox is not present in pacakges tab of Gluster Wizard")
                if "Packages" in labels_list:
                    log.info("Packages textbox is present in packages tab of Gluster Wizard")
                else:
                    log.error("Packages textbox is not present in packages tab of Gluster Wizar")
                if dr.find_element_by_xpath("//label[@class='control-label']").text == "Update Hosts":
                    log.info("Update Hosts textbox check box is present in packages tab of Gluster Wizard")
                else:
                    log.error("Update Hosts textbox check box is not present in packages tab of Gluster Wizard")
                dr.save_screenshot('screenshots/pacakges_tab.png')
                
                    
            else:
                log.info ("os variant is %s" %ret0)
                elements = dr.find_elements_by_xpath("//label[@class='col-md-2 control-label']")
                labels_list = []
                for labels in elements:
                    label = labels.text
                    labels_list.append(label)
                if "Repositories" in labels_list:
                    log.info("Repositories textbox is present in pacakges tab of Gluster Wizard")
                else:
                    log.error("Repositories textbox is not present in pacakges tab of Gluster Wizard")
                if "Packages" in labels_list:
                    log.info("Packages textbox is present in packages tab of Gluster Wizard")
                else:
                    log.error("packages textbox is not present in pacakges tab of Gluster Wizard")
                if "CDN Username" in labels_list:
                    log.info("CDN User name textbox is present in packages tab of Gluster Wizard")
                else:
                    log.error("CDN User name textbox is not present in pacakges tab of Gluster Wizard")
                if "CDN Password" in labels_list:
                    log.info("CDN Password textbox is present in packages tab of Gluster Wizard")
                else:
                    log.error("CDN Password textbox is not present in pacakges tab of Gluster Wizard")
                if "Pool ID" in labels_list:
                    log.info("Pool ID textbox is present in packages tab of Gluster Wizard")
                else:
                    log.error("Pool ID textbox is not present in pacakges tab of Gluster Wizard")
                if dr.find_element_by_xpath("//label[@class='control-label']").text == "Update Hosts":
                    log.info("Update Hosts check box is present in packages tab of Gluster Wizard")
                else:
                    log.error("Update Hosts textbox check box is not present in packages tab of Gluster Wizard")
                dr.save_screenshot('screenshots/pacakges_tab_RHEL.png')
    dr.quit()
            
            
def runtest():
    #check_cleanup_of_gluster_setup_done()
    check_deployment_with_hostedengine_on_gluster()
    
    
