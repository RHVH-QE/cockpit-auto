from utils.helpers import RhevmAction
from utils.page_objects import PageObject, PageElement, MultiPageElement
from fabric.api import run


class NodeStatusPage(PageObject):
    """To check Node status and System info on Virtualization panel."""
    # health_status_btn: click health_status_text link_text
    health_status_btn = PageElement(
        xpath=".//*[@id='content']/div/div/div[1]/table/tbody[2]/tr[1]/td[2]/div[1]/a/div")

    # currentlayer_status_btn: click currentlayer_status_text link_text
    currentlayer_status_btn = PageElement(
        xpath=".//*[@id='content']/div/div/div[1]/table/tbody[2]/tr[2]/td[2]/div[1]/a")

    # rollback_btn: click rollback button
    rollback_btn = PageElement(
        xpath=".//*[@id='content']/div/div/div[1]/table/tbody[2]/tr[2]/td[2]/div[1]/span/button")

    # strong text shown after Virtual Machines
    strong_txt = MultiPageElement(tag_name="strong")

    # page_links: link text after Network info, System log, storage, SSH host key
    page_links = MultiPageElement(link_text="View")

    # accordion_header_btn: like "Thin storage","basic storage","Mount points" button
    accordion_header_btn = MultiPageElement(class_name="accordion-header")
    # close_btn : close button,like "X"
    close_btn = MultiPageElement(class_name="close")

    # elements under Node health dialog
    ok_icons = MultiPageElement(class_name="pficon-ok")

    # elements under Node information dialog
    entry_txts = MultiPageElement(class_name="col-md-6")

    # elements under rollback dialog
    available_layer_txt = MultiPageElement(class_name="col-md-8")

    # elements with warning if login with non-root account
    alert_div_span = PageElement(xpath=".//*[@id='content']/div/div[1]/span")
    alert_div = PageElement(class_name="alert-danger")

    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(NodeStatusPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.health_status_btn, "Health status btn not exist"
            assert self.currentlayer_status_btn, \
                "Currentlayer status button not exist"
            assert self.rollback_btn, "Rollback btn not exist"
        self.wait()

    def query_host_is_registerd(self, rhvm_fqdn, host_name):
        rhvm_action = RhevmAction(rhvm_fqdn)
        result = rhvm_action.query_host_id_by_name(host_name)
        return result

    def add_host_to_rhvm(self, rhvm_fqdn, host_ip, host_name, host_password):
        rhvm_action = RhevmAction(rhvm_fqdn)
        rhvm_action.add_new_host(host_ip, host_name, host_password)
        self.wait(120)

    def remove_host_from_rhvm(self, rhvm_fqdn, host_name):
        rhvm_action = RhevmAction(rhvm_fqdn)
        rhvm_action.remove_host(host_name)
        self.wait(10)

    def check_virtual_machine(self):
        """
        Purpose:
            Check the virtual Machines in oVirt page
        """
        raise NotImplementedError

    def check_node_status(self):
        """
        Purpose:
            Check node status in virtualization dashboard.
        """
        with self.switch_to_frame(self.frame_right_name):
            assert self.health_status_btn, "Health status btn not exist"
            assert self.currentlayer_status_btn, \
                "Currentlayer status button not exist"
            assert self.rollback_btn, "Rollback btn not exist"
        self.wait()

    def _check_vdsmd_active(self):
        cmd = "systemctl status vdsmd|grep Active"
        output_status = run(cmd)
        status = output_status.split()[1]
        return status

    def check_node_health(self, is_registerd=True):
        """
        Purpose:
            Check node health info in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.health_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list[0:3]:
                i.click()
            self.wait(10)
            ok_number = len(list(self.ok_icons))

            if is_registerd:
                assert ok_number == 14, "Node health status is error"
            else:
                if self._check_vdsmd_active() == "active":
                    assert ok_number == 14, "Node health status is error"
                else:
                    assert ok_number == 11, "Node health status is error"
            close_btn_list = list(self.close_btn)
            for j in close_btn_list[0:]:
                j.click()

    def check_node_info(self, test_layer):
        """
        Purpose:
            Check node information in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.currentlayer_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list:
                i.click()
            self.wait(3)

            # Current layer should be identical with the argument
            entry_txt_list = list(self.entry_txts)
            assert entry_txt_list[1].text == test_layer, \
                "Test layer fail"

            # Since no update action on the new fresh installed
            # system, default layer is current layer
            assert entry_txt_list[0].text == entry_txt_list[1].text, \
                "Default is not current layer"

            close_btn_list = list(self.close_btn)
            for j in close_btn_list[0:]:
                j.click()

    def check_node_layer(self, test_layer):
        """
        Purpose:
            Check node layers in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.currentlayer_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list:
                i.click()
            self.wait(3)

            # Current layer should be identical with the argument
            entry_txt_list = list(self.entry_txts)
            assert entry_txt_list[1].text == test_layer, \
                "Test layer fail"

            # Since no update action on the new fresh installed
            # system, default layer is current layer
            assert entry_txt_list[0].text == entry_txt_list[1].text, \
                "Default is not current layer"

            close_btn_list = list(self.close_btn)
            for j in close_btn_list[0:]:
                j.click()

    def check_node_status_fc(self, test_layer, is_registerd=True):
        """
        Purpose:
            Check node status with FC multipath
        """
        # This will be tested on a rhvh with fc storage
        self.check_node_status()
        self.check_node_health()
        self.check_node_info(test_layer)

    def check_node_status_efi(self, test_layer, is_registerd=True):
        """
        Purpose:
            Check node status with EFI
        """
        self.check_node_status()
        self.check_node_health(is_registerd)
        self.check_node_info(test_layer)

    def check_rollabck_func(self):
        """
        Purpose:
            Rollback funciton in virtualization dashboard
        """
        raise NotImplementedError

    def check_network_func(self):
        """
        Purpose:
            Check the Networking Information in virtualization dashboard
        """
        # Since no network info on cockpit, just drop this case currently
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            page_links_list = list(self.page_links)
            system_logs_link = page_links_list[0]
            system_logs_link.click()
            self.wait(3)

    def check_system_log(self):
        """
        Purpose:
            Check the System Logs in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            page_links_list = list(self.page_links)
            system_logs_link = page_links_list[1]
            system_logs_link.click()
            self.wait(3)

    def check_storage(self):
        """
        Purpose:
            Check the Storage in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            page_links_list = list(self.page_links)
            storage_link = page_links_list[2]
            storage_link.click()
            self.wait(3)

    def check_ssh_key(self):
        """
        Purpose:
            Check the ssh host key in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            page_links_list = list(self.page_links)
            storage_link = page_links_list[3]
            storage_link.click()
            self.wait(3)

    def check_list_vms(self):
        """
        Purpose:
            List of vms in dashboard
        """
        with self.switch_to_frame(self.frame_right_name):
            cmd = "ps -ef|grep qemu-kvm|grep -v grep|wc -l"
            output = run(cmd)
            vm_count = int(output)
            assert int(list(self.strong_txt)[0].text) == vm_count, \
                "VM count not correct"
        self.wait()

    def check_non_root_alert(self, default=False):
        """
        Purpose:
            Check if login with non-root account, if yes, there
            will be a alert div
        """
        with self.switch_to_frame(self.frame_right_name):
            if default:
                try:
                    assert self.alert_div,  \
                        "Can't check node status! Please run as administrator not exists"
                except Exception as e:
                    assert False, "Can't check node status! Please run as administrator not exists"
