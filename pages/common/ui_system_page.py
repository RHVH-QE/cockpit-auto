import re
from utils.page_objects import PageObject, PageElement, MultiPageElement
from fabric.api import settings, run


class SystemPage(PageObject):
    brand_log = PageElement(id_="index-brand")
    machine_link = PageElement(
        xpath=".//*[@id='machine-link']/span")
    hostname_btn = PageElement(
        id_="system_information_hostname_button")
    systime_btn = PageElement(
        id_="system_information_systime_button")
    performance_profile_btn = PageElement(class_name="action-trigger")

    # Elements after click the hostname_btn
    pretty_hostname_input = PageElement(id_="sich-pretty-hostname")
    real_hostname_input = PageElement(id_="sich-hostname")
    set_hostname_apply_btn = PageElement(id_="sich-apply-button")

    # Elements after click the systime_btn
    timezone_input = PageElement(class_name="form-control")
    set_time_btn = PageElement(class_name="btn-default")
    set_time_apply_btn = PageElement(id_="systime-apply-button")

    # Elements after click performance profile button
    performance_profiles = MultiPageElement(class_name="list-group-item")
    performance_apply_btn = PageElement(class_name="btn-primary")

    # frame name
    frame_right_name = "cockpit1:localhost/system"

    def __init__(self, *args, **kwargs):
        super(SystemPage, self).__init__(*args, **kwargs)
        self.get("/system")
        self.wait(5)

    def basic_check_elements_exists(self):
        assert self.brand_log, "brand-log not exist"
        self.wait(2)

    def check_login_host(self, host_ip):
        assert re.search(host_ip, self.machine_link.text),   \
            "%s not login" % host_ip

    def configure_hostname(self):
        """
        Purpose:
            Configure hostname on system page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.hostname_btn.click()
            self.wait(1)
            self.pretty_hostname_input.send_keys("cockpitauto")
            self.real_hostname_input.clear()
            self.wait(1)
            self.real_hostname_input.send_keys("cockpitauto.redhat.com")
            self.wait(1)
            self.set_hostname_apply_btn.click()
            self.wait(1)

    def check_configure_hostname(self):
        """
        Purpose:
            Check the hostname were changed
        """
        with self.switch_to_frame(self.frame_right_name):
            assert re.search(
                "cockpitauto.redhat.com",
                self.hostname_btn.text),    \
                "Configure hostname failed"

        with settings(warn_only=True):
            cmd = "hostname"
            output = run(cmd)
            assert re.search("cockpitauto.redhat.com", output),    \
                "Configure hostname failed"

    def configure_timezone(self):
        """
        Purpose:
            Configure timezone on system page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.systime_btn.click()
            self.wait(3)

            self.timezone_input.clear()
            self.wait(1)
            self.timezone_input.send_keys("America/Los_Angeles")
            self.wait(1)
            self.set_time_apply_btn.click()

    def check_configure_timezone(self):
        """
        Purpose:
            Check time were configured as needed
        """
        with settings(warn_only=True):
            cmd = "timedatectl|grep 'Time zone'"
            output = run(cmd)
            assert re.search("America/Los_Angeles", output),    \
                "Configure hostname failed"

    def configure_time(self):
        """
        Purpose:
            Configure time on system page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.systime_btn.click()
            self.wait(1)

            # To do
            pass

    def check_configure_time(self):
        """
        Purpose:
            Check the time were configured as needed
        """
        with settings(warn_only=True):
            # To do
            pass

    def change_performance_profile(self):
        """
        Purpose:
            Change the performance profile
        """
        with self.switch_to_frame(self.frame_right_name):
            self.performance_profile_btn.click()
            self.wait(1)

            list(self.performance_profiles)[1].click()
            self.wait(0.5)
            self.performance_profile_btn.click()
            self.wait(1)

    def check_change_performance_profile(self):
        """
        Purpose:
            Check the profile is changed
        """
        with settings(warn_only=True):
            cmd = "tuned-adm active"
            output = run(cmd)

            assert re.search("balanced", output),   \
                "The profile is not changed"
