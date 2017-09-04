import os
import re
from utils.page_objects import PageObject, PageElement, MultiPageElement
from fabric.api import run, get, env
from StringIO import StringIO


class SubscriptionsPage(PageObject):
    """Subscription-manager for host to register to RHSM/Satellite server"""

    ######################

    register_sys_btn = PageElement(tag_name="button")
    login_input = PageElement(id_="subscription-register-username")
    passwd_input = PageElement(id_="subscription-register-password")
    key_input = PageElement(id_="subscription-register-key")
    org_input = PageElement(id_="subscription-register-org")

    btns = MultiPageElement(tag_name="button")

    # url = PageElement(id_="subscription-register-url")
    url_select_btn = PageElement(
        xpath=".//*[@id='subscription-register-url']/button")
    url_default_item = PageElement(
        xpath=".//*[@id='subscription-register-url']/ul/li[1]/a")
    url_custom_item = PageElement(
        xpath=".//*[@id='subscription-register-url']/ul/li[2]/a")
    url_input = PageElement(id_="subscription-register-url-custom")

    installed_product_btn = PageElement(tag_name="th")
    spans = MultiPageElement(tag_name="span")

    # frame name
    frame_right_name = "cockpit1:localhost/subscriptions"

    def __init__(self, *args, **kwargs):
        super(SubscriptionsPage, self).__init__(*args, **kwargs)
        self.get("/subscriptions")
        self.wait(10)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.register_sys_btn, "register system btn not exist"
            assert self.login_input, "login text editor not exist"
            assert self.passwd_input, "password text editor not exist"
            assert self.submit_btn, "register button not exist"
            assert self.key_input, "Activation Key text editor not exist"
            assert self.org_input, "Organization text editor not exist"
            assert self.url_select_btn, "Url select btn not exist"
            assert self.url_default_item, "default item in url list not exist"
            assert self.url_custom_item, "custom item in url list not exist"
            assert self.url_input, "url text editor not exist"

    def check_register_rhsm(self, rhn_user, rhn_password):
        """
        Purpose:
            Test subscription to RHSM
        """
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self._clean_all()
            self.url_select_btn.click()
            self.url_custom_item.click()
            self.wait(0.5)
            self.login_input.send_keys(rhn_user)
            self.wait(0.5)
            self.passwd_input.send_keys(rhn_password)
            self.wait(0.5)

            submit_btn = list(self.btns)[3]
            submit_btn.click()
            self.wait(60)

    def check_register_rhsm_key_org(self, activation_key, activation_org):
        """
        Purpose:
            Test subscription to RHSM with key and organization
        """
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self._clean_all()
            self.url_select_btn.click()
            self.url_custom_item.click()
            self.wait(0.5)
            self.key_input.send_keys(activation_key)
            self.wait(0.5)
            self.org_input.send_keys(activation_org)
            self.wait(0.5)

            submit_btn = list(self.btns)[3]
            submit_btn.click()
            self.wait(60)

    def check_register_satellite(self, satellite_ip, satellite_user, satellite_password):
        """
        Purpose:
            RHEVM-16752
            Test subscription to Satellite server
        """
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self._clean_all()
            self.url_select_btn.click()
            self.url_custom_item.click()
            self.wait(0.5)
            self.url_input.send_keys(satellite_ip + "/rhsm")
            self.wait(0.5)
            self.login_input.send_keys(satellite_user)
            self.wait(0.5)
            self.passwd_input.send_keys(satellite_password)
            self.wait(0.5)
            self.submit_btn.click()
            self.wait(60)

    def check_password_encrypted(self, rhn_password):
        """
        Purpose:
            RHEVM-16750
            Test check password is encrypted in rhsm.log
        """
        remote_path = "/var/log/rhsm/rhsm.log"
        fd = StringIO()
        get(remote_path, fd)
        content = fd.getvalue()
        assert not re.search(rhn_password, content), "There is plain password in rhsm.log file"

    def check_subscription_result(self):
        with self.switch_to_frame(self.frame_right_name):
            self.installed_product_btn.click()
            self.wait(1)
            product_name = list(self.spans)[0]
            register_status = list(self.spans)[4]
            print product_name.text, register_status.text
            assert product_name.text == "Red Hat Virtualization Host", \
                "product name is wrong"
            assert register_status.text == "Subscribed", \
                "subscription fail"

    def unregister_subsciption(self):
        cmd = 'subscription-manager unregister'
        subscripted = run(cmd)
        self.wait(5)
        if subscripted != "System has been unregistered":
            self.wait(5)

    def ca_install(self, ca_path):
        cmd_download_ca = "curl -O -k " + ca_path
        run(cmd_download_ca)
        self.wait(5)
        cmd_install_ca = "rpm -Uvh " + os.path.basename(ca_path)
        run(cmd_install_ca)
        self.wait(10)

    def add_domain_name(self, ip, hostname):
        append_txt = ip + '  ' + hostname
        cmd_dns = "echo " + append_txt + " >> /etc/hosts"
        run(cmd_dns)

    def _clean_all(self):
        self.login_input.clear()
        self.passwd_input.clear()
        self.key_input.clear()
        self.org_input.clear()

    def reset(self, ca_path):
        cmd_rpm_qa = "rpm -qa|grep katello"
        result = run(cmd_rpm_qa)
        if result:
            cmd = "rpm -e " + os.path.splitext(os.path.basename(ca_path))[0]
            run(cmd)
            self.wait()
