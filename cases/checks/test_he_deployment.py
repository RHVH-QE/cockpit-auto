import os
import re
import json
import time
import urllib2
import logging
from vncdotool import api
from selenium import webdriver
from fabric.api import run, settings, put, local, get, env
from utils.htmlparser import MyHTMLParser
from pages.hosted_engine_page import HePage
from cases.helpers import CheckBase
from utils.htmlparser import MyHTMLParser
from utils.constants import PROJECT_ROOT
from utils.rhvmapi import RhevmAction


log = logging.getLogger("bender")


class TestHostedEngine(CheckBase):
    page = None

    def set_page(self):
        self.page = HePage(self._driver)

    def _get_latest_rhvm_appliance(self, appliance_path):
        """
        Purpose:
            Get the latest rhvm appliance from appliance parent path
        """
        log.info("Getting the latest rhvm4.2 appliance...")
        req = urllib2.Request(appliance_path)
        rhvm_appliance_html = urllib2.urlopen(req).read()

        mp = MyHTMLParser()
        mp.feed(rhvm_appliance_html)
        mp.close()
        mp.a_texts.sort()

        link_42 = []
        all_link = mp.a_texts
        for link in all_link:
            if "4.2" in link:
                link_42.append(link)

        latest_rhvm_appliance_name = link_42[-1]
        latest_rhvm_appliance = appliance_path + latest_rhvm_appliance_name
        return latest_rhvm_appliance

    def _install_rhvm_appliance(self):
        log.info("Getting and installing the latest rhvm appliance ...")
        rhvm_appliance_link = self._get_latest_rhvm_appliance(self._config['rhvm_appliance_path'])
        local_rhvm_appliance = "/root/%s" % rhvm_appliance_link.split('/')[-1]
        output = self.run_cmd("curl -o %s %s" % (local_rhvm_appliance, rhvm_appliance_link))
        if output[0]=="False":
            log.error("Failed to download the latest rhvm appliance...")
        
        self.run_cmd("rpm -ivh %s --force" % local_rhvm_appliance)
        self.run_cmd("rm -rf %s" % local_rhvm_appliance)

    def _add_to_etc_host(self):
        log.info("Adding the host to /etc/hosts...")
        host_name = self.run_cmd("hostname")[1]
        self.run_cmd("echo '%s  %s' >> /etc/hosts" % (self.host_string, host_name))
        self.run_cmd("echo '%s' > /etc/hostname" % host_name)
        self.run_cmd("hostname %s" % host_name)
        self.run_cmd("echo '%s  %s' >> /etc/hosts" % (self._config['he_vm_ip'], self._config['he_vm_fqdn']))

    def _clean_nfs_storage(self, nfs_path):
        log.info("Cleaning the he nfs storage...")
        with settings(
                host_string=self._config['nfs_ip'],
                user="root",
                password=self._config['nfs_password'],
                disable_known_hosts=True,
                connection_attempts=60):
            run("rm -rf %s/*" % nfs_path)

    def _move_failed_setup_log(self):
        log.info("Moving the failed ovirt-hosted-engine-setup.log to the old dir...")
        ret = self.run_cmd("find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log")
        if ret[0] == True:
            if os.path.exists("/var/old_failed_setup_log") == False:
                self.run_cmd("mkdir -p /var/old_failed_setup_log")
            self.run_cmd("mv /var/log/ovirt-hosted-engine-setup/*.log \
                         /var/old_failed_setup_log/")
        else:
            pass

    def _subscription_to_rhsm(self, serverurl, user, password):
        log.info("Subscription to rhn stage ...")
        self.run_cmd("subscription-manager register --serverurl=%s --username=%s \
                     --password=%s" % (serverurl, user, password))
        self.run_cmd("subscription-manager attach --auto")
        self.run_cmd("subscription-manager repos --enable=rhel-7-server-rhvh-4*")
        output = self.run_cmd("subscription-manager repos --list-enable |grep 'Repo ID'|grep 'rhvh'")
        if output == 0:
            log.error("Failed to find the rhvh repos...")

    def _wait_host_status(self, rhvm_ins, host_name, expect_status):
        log.info("Waitting for the host %s" % expect_status)
        i = 0
        host_status = "unknown"
        while True:
            if i > 50:
                raise RuntimeError(
                    "Timeout waitting for host %s as current host status is: %s"
                    % (expect_status, host_status))
            host_status = rhvm_ins.list_host("name", host_name)['status']
            log.info("HOST: %s" % host_status)
            if host_status == expect_status:
                break
            elif host_status == 'install_failed':
                raise RuntimeError("Host is not %s as current status is: %s" %
                                   (expect_status, host_status))
            elif host_status == 'non_operational':
                raise RuntimeError("Host is not %s as current status is: %s" %
                                   (expect_status, host_status))
            time.sleep(10)
            i += 1

    def _set_up(self):
        #super(TestHostedEngine, self).setup()
        try:
            self._move_failed_setup_log()
            self._install_rhvm_appliance()
            self._add_to_etc_host()
            self._clean_nfs_storage(self._config['he_install_nfs'])
        except Exception as e:
            log.info("Failed to init the HostedEngine ENV...")
            return False, e
        return True

    def _he_install(self):
        # Setup the HostedEngine ENV
        self._set_up()
        try:
            # VM page
            with self.page.switch_to_frame(self.page.frame_right_name):
                log.info("Starting to deploy HostedEngine...")
                self.page.deploy_icon.click()
                self.page.wait(10)
                # MAC Address
                log.info("Input the VM MAC Address...")
                self.page.mac_address.clear()
                self.page.wait(2)
                self.page.mac_address.send_keys(self._config['he_vm_mac'])
                self.page.wait(1)
                # VM hostname
                log.info("input the Engine hostname...")
                self.page.engine_hostname.clear()
                self.page.wait(1)
                self.page.engine_hostname.send_keys(self._config['he_vm_fqdn'].split(".")[0])
                self.page.wait(1)
                # Domain name
                log.info("Input the domain name...") 
                self.page.domain_name.clear()
                self.page.wait(1)
                self.page.domain_name.send_keys(self._config['he_vm_domain'])
                self.page.wait(1)
                # VM root password
                log.info("Input the VM root password...")
                self.page.passwd[0].send_keys(self._config['he_vm_password'])
                self.page.wait(1)
                self.page.passwd[1].send_keys(self._config['he_vm_password'])
                self.page.wait(1)
                self.page.next_button.click()
                self.page.wait(5)

                # Engine page
                log.info("Input the Engine admin password...")
                self.page.passwd[2].send_keys(self._config['engine_password'])
                self.page.wait(1)
                self.page.passwd[3].send_keys(self._config['engine_password'])
                self.page.wait(1)
                self.page.next_button.click()
                self.page.wait(5)

                # Storage page
                log.info("Input the HE-VM Storage path")
                nfs_path = self._config['nfs_ip'] + ':' +self._config['he_install_nfs']
                self.page.nfs_path.send_keys(nfs_path)
                self.page.wait(1)
                self.page.next_button.click()
                self.page.wait(5)

                # Network page
                log.info("Configure the Network page...")
                self.page.next_button.click()
                self.page.wait(5)

                # Review page
                log.info("Review all the configure about HostedEngine...")
                self.page.deploy_button.click()
                self.page.wait(50)
                log.info("Select the appliance...")
                self.page.default_button[2].click()

                self.page.wait(1400)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_he_install(self):
        true, false = True, False
        vm_status = {'detail': 'Up', 'health': 'good', 'vm': 'up'}
        log.info("Checking HostedEngine install...")
        try:
            self._he_install()
            ret = self.run_cmd("hosted-engine --check-deployed")
            ret_st = self.run_cmd("hosted-engine --vm-status --json")
            
            if ret[0] == True:
                if json.loads(ret_st[1])['1']['engine-status'] == vm_status:
                    log.info("HE is deployed on %s and HE-VM is up" % self.host_string)
                else:
                    log.info("HE is deployed on %s but HE-VM is not up" % self.host_string)
                    return False
            else:
                log.error("HE is not deployed on %s" % self.host_string)
                return False

            ret_log = self.run_cmd("find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log")
            if ret_log[0] == True:
                log.info("Hosted Engine setup log found")
            else:
                log.error("No hosted engine setup log found")
                return False

            he_res = self.run_cmd("grep 'Hosted Engine successfully deployed' %s" % ret_log[1])
            if he_res[0] == True:
                log.info("Found the successfully message in the setup log %s" % he_res[1])
            else:
                log.error("Not found the succeddfully message in the setup log %s" % he_res[1])
                return False

        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_he_hint(self):
        log.info("Check the local maintenance on one host hint...")
        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.check_local_maintenance_hint()
                self.page.wait(5)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_engine_status(self):
        log.info("Check the engine status")
        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                self.page.check_engine_status()
                self.page.wait(5)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_vm_status(self):
        try:
            with self.page.switch_to_frame(self.page.frame_right_name):
                log.info("Check he running on the host...")
                self.page.check_he_running_on_host(self.run_cmd("hostname")[1])
                self.page.wait(2)
                log.info("Check HE-VM status...")
                self.page.check_vm_status()
                self.page.wait(5)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_no_password_saved(self):
        log.info("Checking no password saved in the log file...")
        try:
            ret_log = self.run_cmd("find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log")
            output_engine_passwd = self.run_cmd("grep 'adminPassword=str' %s |awk -F ':' '{printf $5}'" % ret_log[1])
            output_root_passwd = self.run_cmd("grep 'cloudinitRootPwd=str' %s |awk -F ':' '{printf $5}'" % ret_log[1])
            if self._config['engine_password'] not in output_engine_passwd[1] and self._config['he_vm_password'] not in output_root_passwd:
                log.info("There is no engine admin or root password saved in the log file...")
                return True
            else:
                log.info("Found the password text saved in the log file...")
                return False
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_no_large_messages(self):
        log.info("Check if there are a large number of redundant log generation in /var/log/messages.")
        size1 = self.run_cmd("ls -lnt /var/log/messages | awk '{print $5}'")
        time.sleep(10)
        size2 = self.run_cmd("ls -lnt /var/log/messages | awk '{print $5}'")
        if int(size2[1]) - int(size1[1]) > 200:
            log.info("There are a large redundant log generation in /var/log/messages")
            return False
        else:
            log.info("There are no large redundant log generation in /var/log/messages")
            return True

    def check_additional_host(self):
        log.info("Check the additional host in the cluster as HostedEngine deployment...")
        
        self._clean_nfs_storage(self._config['he_data_nfs'])
        rhvm_fqdn = self._config['he_vm_fqdn']
        host_name = self.run_cmd("hostname")[1]
        rhvm = RhevmAction(rhvm_fqdn, "admin", self._config['engine_password'])

        try:
            log.info("Add the HE first data domain... ")
            rhvm.add_plain_storage_domain(self._config['sd_name'], "data", "nfs", self._config['nfs_ip'], self._config['he_data_nfs'], host_name)
            time.sleep(100)

            log.info("Attach the data storage to the datacenter...")
            rhvm.attach_sd_to_datacenter(self._config['sd_name'], "Default")
            time.sleep(15)
            
            log.info("Add the additional host to the cluster...")
            rhvm.add_host(self._config['second_host'], self._config['second_vm_fqdn'], self._config['second_password'], "Default", True)
            self._wait_host_status(rhvm, self._config['second_vm_fqdn'], 'up')
            time.sleep(10)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_put_local_maintenance(self):
        log.info("Check put the host to local maintenance...")
        try:
            
            self.page.check_three_buttons()
            self.page.wait(5)
            self.page.put_host_to_local_maintenance()
            self.page.wait(10)

            self.page.check_host_in_local_maintenance()

        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_migrate_he(self):
        log.info("Check whether he on additional host successfully...")
        try:
            if self.page.check_host_not_in_local_maintenance == True:
                self.check_put_local_maintenance()

            time.sleep(10)
            self.page.check_vm_on_additional_host()
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_remove_from_maintenance(self):
        log.info("Check remove this host from maintenance...")
        try:
            self.page.wait(2)
            self.page.remove_host_from_local_maintenance()
            self.page.wait(5)
            self.page.check_host_not_in_local_maintenance()
            self.page.check_cluster_not_in_global_maintenance()
            self.page.wait(2)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_put_global_maintenance(self):
        log.info("Check the cluster in the global maintenance...")
        try:
            self.page.put_cluster_to_global_maintenance()
            self.page.wait(6)
            self.page.check_cluster_in_global_maintenance()
            self.page.wait(5)
        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_he_clean(self):
        log.info("Check the function to clean he env is OK, then you can redeploy the HE...")
        try:
            local_path = os.path.join(PROJECT_ROOT, 'utils', 'clean_he_env.py')
            self.put_remote_file(local_path, "/root/clean_he_env.py")
            self.run_cmd("python /root/clean_he_env.py")
            time.sleep(10)
            state = "You must run deploy first"
            if self.run_cmd("hosted-engine --vm-status")[1] == state:
                log.info("Clean the he env is OK...")
                return True
            else:
                return False

        except Exception as e:
            log.exception(e)
            return False
        return True

    def check_he_redeploy(self):
        log.info("Check trying to redeploy HostedEngine on the host...")
        try:
            self._driver.refresh()
            self.page.wait(5)
            self.check_he_install()
        except Exception as e:
            log.exception(e)
            return False
        return True
