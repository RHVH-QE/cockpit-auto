import re
from utils.page_objects import PageObject, PageElement, MultiPageElement
from fabric.api import run, settings


class ServicePage(PageObject):
    targets_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[1]")
    sys_service_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[2]")
    sockets_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[3]")
    timers_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[4]")
    paths_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[5]")

    # Elements under the system service button
    test_services_state = MultiPageElement(class_name="service-unit-data")
    test_services_description = MultiPageElement(
        class_name="service-unit-description")

    # Elements after click above service button
    service_title_name = PageElement(
        xpath=".//*[@id='service']/ol/li[2]")
    service_start_stop_action = PageElement(
        xpath=".//*[@id='service-unit-action']/button[1]")
    service_enable_disable_action = PageElement(
        xpath=".//*[@id='service-file-action']/button[1]")
    service_unit_dropdown_action = PageElement(
        xpath=".//*[@id='service-unit-action']/button[2]")
    service_file_dropdown_action = PageElement(
        xpath=".//*[@id='service-file-action']/button[2]")

    service_restart_action = PageElement(
        xpath=".//*[@id='service-unit-action']/ul/li[3]/a")

    # frame name
    frame_right_name = "cockpit1:localhost/system/services"

    def __init__(self, *args, **kwargs):
        super(ServicePage, self).__init__(*args, **kwargs)
        self.get("/system/services")
        self.wait(5)

    def basic_check_elements_exists(self):
        assert self.targets_btn, "targets button not exists"
        assert self.sys_service_btn, "system service button not exists"
        assert self.sockets_btn, "socket button not exists"
        assert self.timers_btn, "timers button not exists"
        assert self.paths_btn, "paths button not exists"

    def disable_service_action(self):
        with self.switch_to_frame(self.frame_right_name):

            # Get a running service to disable
            for k in range(len(list(self.test_services_state))):
                if re.search(
                        "running", list(self.test_services_state)[k].text):
                    running_seq = k
                    break

            list(self.test_services_description)[running_seq].click()
            self.wait(1)

            # Get the running service name and click disable
            service_name = self.service_title_name.text
            self.service_enable_disable_action.click()
            self.wait(1)
            return service_name

    def check_service_is_disabled(self, service_name):
        # Check the service is disabled
        with settings(warn_only=True):
            cmd = "service %s status|grep Loaded" % service_name
            output = run(cmd)
        assert re.search("disabled", output.split(';')[1]),   \
            "Failed to disable %s" % service_name

    def enable_service_action(self):
        with self.switch_to_frame(self.frame_right_name):
            # Click enable button to enable the service
            self.service_enable_disable_action.click()

    def check_service_is_enabled(self, service_name):
        # Check the service is disabled
        with settings(warn_only=True):
            cmd = "service %s status|grep Loaded" % service_name
            output = run(cmd)
        assert re.search("enabled", output.split(';')[1]),   \
            "Failed to enable %s" % service_name

    def stop_service_action(self):
        with self.switch_to_frame(self.frame_right_name):
            # Click enable button to enable the service
            self.service_start_stop_action.click()

    def check_service_is_stoped(self, service_name):
        with settings(warn_only=True):
            cmd = "service %s status|grep Active" % service_name
            output = run(cmd)

        assert re.search("inactive", output),   \
            "Failed to stop %s service" % service_name

    def start_service_action(self):
        with self.switch_to_frame(self.frame_right_name):
            self.service_start_stop_action.click()

    def check_service_is_started(self, service_name):
        with settings(warn_only=True):
            cmd = "service %s status|grep Active" % service_name
            output = run(cmd)

        assert re.search("active", output),   \
            "Failed to start %s service" % service_name

    def restart_service_action(self):
        with self.switch_to_frame(self.frame_right_name):
            self.service_unit_dropdown_action.click()

            # Restart unit action
            self.service_restart_action.click()

    def check_service_is_restarted(self, service_name):
        with settings(warn_only=True):
            cmd = "service %s status|grep Active" % service_name
            output = run(cmd)

        assert re.search("active", output),   \
            "Failed to restart the %s service" % service_name
