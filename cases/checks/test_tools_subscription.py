import logging
import re
from pages.tools_subscription_page import SubscriptionPage
from cases.helpers import CheckBase
from StringIO import StringIO


log = logging.getLogger('sherry')


class TestSubscription(CheckBase):
    page = None

    def set_page(self):
        self.page = SubscriptionPage(self._driver)

    def _clean_all(self):
        self.page.login_input.clear()
        self.page.passwd_input.clear()
        self.page.key_input.clear()
        self.page.org_input.clear()

    def _register_submit(self):
        for btn in list(self.page.apply_cancel_btns):
            if btn.text == "Register":
                btn.click()

    def _check_subscription_result(self):
        status_content = list(self.page.details_contents)[4]
        assert status_content.text == "Subscribed", \
            "subscription fail"

    def _check_cert_file(self):
        cmd = "ls /etc/pki/product-default/328.pem"
        ret = self.run_cmd(cmd)
        assert ret[0], "No 328.pem file found"
    
    def _check_repos(self):
        cmd = "subscription-manager repos --list|grep rhel-7-server-rhvh-4*"
        ret = self.run_cmd(cmd)
        assert ret[0], "No rhel-7-server-rhvh-4* repo found"

        cmd = "subscription-manager repos  --enable=rhel-7-server-rhvh-4*"
        ret = self.run_cmd(cmd)
        assert ret[0], "rhel-7-server-rhvh-4* can not be enabled"
    
    def _search_packages(self):
        packages = ['tcpdump', 'vim-enhanced', 'screen', 'strace', 
            'ltrace', 'wget', 'sysstat', 'dropwatch', 'systemtap', 'rhvm-appliance']
        for pak in packages:
            cmd = "yum search {}".format(pak)
            ret = self.run_cmd(cmd)
            assert ret[0], "Can not find package {}".format(pak)

    def _unregister_subsciption(self):
        cmd = 'subscription-manager unregister'
        self.run_cmd(cmd)
        self.page.wait(5)

    def _check_passwd_encrypted(self):
        rhn_password = self._config['rhn_password']
        remote_file = "/var/log/rhsm/rhsm.log"
        fd = StringIO()
        self.get_remote_file(remote_file, fd)
        content = fd.getvalue()
        assert not re.search(rhn_password, content), \
            "There is plain password in rhsm.log file"

    def check_register_rhsm(self):
        """
        Purpose:
            Subscription to RHSM
        """
        log.info('Subscription to RHSM...')

        cmd = "cat /usr/share/imgbase/build/meta/nvr"
        ret = self.run_cmd(cmd)
        if ret[0]:
            product_version = ret[1]
        else:
            return False

        try:
            # Check basic elements
            self.page.basic_check_elements_exists(product_version)
        except AssertionError as e:
            log.error(e)
            return False
        try:
            with self.page.switch_to_frame(self.page.frame_right_name):  
                self.page.register_sys_btn.click()
                wev = self.page.wait_until_element_visible
                wev(self.page.register_dialog_title)

                self._clean_all()

                self.page.url_select_btn.click()
                self.page.url_custom_item.click()
                self.page.wait(0.5)

                rhn_user = self._config['rhn_user']
                rhn_password = self._config['rhn_password']
                self.page.login_input.send_keys(rhn_user)
                self.page.wait(0.5)
                self.page.passwd_input.send_keys(rhn_password)
                self.page.wait(0.5)
                
                self._register_submit()
                self.page.wait(60)

                self._check_subscription_result()

            self._check_cert_file()

            self._check_repos()

            self._search_packages()

            self._check_passwd_encrypted
        except Exception as e:
            log.exception(e)
            return False
        finally:
            self._unregister_subsciption()

        return True

    def check_register_rhsm_org(self):
        """
        Purpose:
            Subscription to RHSM with key and organization
        """
        log.info('Subscription to RHSM...')

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):  
                self.page.register_sys_btn.click()
                wev = self.page.wait_until_element_visible
                wev(self.page.register_dialog_title)

                self._clean_all()

                self.page.url_select_btn.click()
                self.page.url_custom_item.click()
                self.page.wait(0.5)

                activation_key = self._config['activation_key']
                activation_org = self._config['activation_org']
                self.page.key_input.send_keys(activation_key)
                self.page.wait(0.5)
                self.page.org_input.send_keys(activation_org)
                self.page.wait(0.5)
                
                self._register_submit()
                self.page.wait(60)

                self._check_subscription_result()

            self._check_cert_file()

        except Exception as e:
            log.exception(e)
            return False
        finally:
            self._unregister_subsciption()
        return True

    def check_register_satellite(self):
        """
        Purpose:
            Subscription to Satellite server
        """
        log.info('Subscription to Satellite server...')

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):  
                self.page.register_sys_btn.click()
                wev = self.page.wait_until_element_visible
                wev(self.page.register_dialog_title)

                self._clean_all()

                self.page.url_select_btn.click()
                self.page.url_custom_item.click()
                self.page.wait(0.5)

                satellite_ip = self._config['satellite_ip']
                satellite_user = self._config['satellite_user']
                satellite_passwd = self._config['satellite_password']
                self.page.url_input.send_keys(satellite_ip+'/rhsm')
                self.page.wait(0.5)
                self.page.login_input.send_keys(satellite_user)
                self.page.wait(0.5)
                self.page.passwd_input.send_keys(satellite_passwd)
                self.page.wait(0.5)
                
                self._register_submit()
                self.page.wait(60)

                self._check_subscription_result()

            self._check_cert_file()

        except Exception as e:
            log.exception(e)
            return False
        finally:
            self._unregister_subsciption()
        return True

    def check_register_satellite57(self):
        """
        Purpose:
            Subscription to Satellite5.7 server
        """
        log.info('Subscription to Satellite5.7 server...')

        try:
            with self.page.switch_to_frame(self.page.frame_right_name):  
                self.page.register_sys_btn.click()
                wev = self.page.wait_until_element_visible
                wev(self.page.register_dialog_title)

                self._clean_all()

                self.page.url_select_btn.click()
                self.page.url_custom_item.click()
                self.page.wait(0.5)

                satellite_ip = self._config['satellite57_ip']
                satellite_user = self._config['satellite57_user']
                satellite_passwd = self._config['satellite57_password']
                self.page.url_input.send_keys(satellite_ip+'/rhsm')
                self.page.wait(0.5)
                self.page.login_input.send_keys(satellite_user)
                self.page.wait(0.5)
                self.page.passwd_input.send_keys(satellite_passwd)
                self.page.wait(0.5)
                
                self._register_submit()
                self.page.wait(60)

                self._check_subscription_result()

            self._check_cert_file()

        except Exception as e:
            log.exception(e)
            return False
        finally:
            self._unregister_subsciption()
        return True
