import re
from utils.page_objects import PageObject, PageElement, MultiPageElement
from utils.helpers import RhevmAction
from selenium.common.exceptions import NoAlertPresentException
from fabric.api import run, env, get
from StringIO import StringIO
from fabric.api import run, settings


class VirtualMachinesPage(PageObject):
    """
    Function:
        Inspect virtual machines which managed by RHEVM in cockpit WebUI
    """
    content_username_txt = PageElement(id_="content-user-name")
    logout_link = PageElement(id_="go-logout")

    running_vms_btn = PageElement(id_="main-btn-menu-hostvms")
    vms_in_cluster_btn = PageElement(id_="main-btn-menu-allvms")
    vdsm_btn = PageElement(id_="main-btn-menu-vdsm")

    technical_preview_text = PageElement(
        xpath=".//*[@id='ovirt-content']/table/tbody/tr/td[2]/div")
    engine_login_link = PageElement(id_="engine-login-title")
    maintenance_host_link = PageElement(link_text="Host to Maintenance")
    refresh_link = PageElement(partial_link_text="Refresh")
    engine_login_passwd_input = PageElement(id_="engine-login-pwd")
    engine_login_url_input = PageElement(id_="engine-login-url")
    engine_login_submit_btn = PageElement(id_="modal-engine-login-form-dologin")

    virtual_machines_title = PageElement(
        xpath=".//*[@id='virtual-machines']/div[1]/div/div[1]/h3")
    total_vms_text = PageElement(id_="host-vms-total")
    vdsm_unactived_textblock = PageElement(id_="vdsm-is-not-active")

    # VM elements
    vm_hostname_links = MultiPageElement(
        xpath=".//*[@id='host-vms-list-item-name-']/a")
    vm_guest_ip_txts = MultiPageElement(
        xpath=".//*[@id='host-vms-list-item-name-']/small[1]")
    vm_hostname_txts = MultiPageElement(
        xpath=".//*[@id='host-vms-list-item-name-']/small[2]")
    vm_up_txts = MultiPageElement(
        xpath=".//*[@id='host-vms-list-item-name-']/small[3]")
    vm_lifecycle_btns = MultiPageElement(tag_name="button")
    vm_lifecycle_operations = MultiPageElement(tag_name="li")

    # Elements under detail of VM
    name_first_row_second_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td[2]")
    ip_first_row_fourth_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[1]/td[4]")
    id_second_row_second_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td[2]")
    vcpu_second_row_fourth_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[2]/td[4]")
    username_third_row_second_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[3]/td[2]")
    uptime_third_row_fourth_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[3]/td[4]")
    display_fourth_row_second_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[4]/td[2]")
    fqdn_fourth_row_fourth_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[4]/td[4]")
    app_fifth_row_second_column = PageElement(
        xpath=".//*[@id='vm-detail-content']/div[2]/table/tbody/tr/td/table/tbody/tr[5]/td[4]")

    # VDSM related elements
    vdsm_service_management_link = PageElement(
        link_text="VDSM Service Management")
    vdsm_conf_textarea = PageElement(id_="editor-vdsm-conf")
    vdsm_save_btn = PageElement(id_="editor-vdsm-btn-save")
    vdsm_reload_btn = PageElement(id_="editor-vdsm-btn-reload")

    vdsm_config_dialog_title = PageElement(id_="modal-confirmation-title")
    vdsm_config_dialog_close_btn = PageElement(class_name="close")
    vdsm_config_dialog_text = PageElement(id_="modal-confirmation-text")
    vdsm_config_dialog_ok = PageElement(id_="modal-confirmation-ok")
    vdsm_config_dialog_cancel = PageElement(
        xpath=".//*[@id='modal-confirmation']/div/div/div[3]/button[1]")
    vdsm_config_dialog_saved = PageElement(id_="editor-vds-conf-msg")

    # sub-frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(VirtualMachinesPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard#/management")
        self.wait(10)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            assert self.running_vms_btn, "Running VMs button is missing"
            assert self.vms_in_cluster_btn, "VMs in cluster button is missing"
            assert self.vdsm_btn, "VDSM button is missing"
            assert self.engine_login_link, "Login to engine link is missing"
            assert self.maintenance_host_link,  \
                "Host to maintenance link is missing"
            assert self.refresh_link, "Refresh link is missing"

    def check_running_vms_unregister(self):
        """
        Purpose:
            Check running VMs (Unregister to RHEVM)
            status in virtual machines page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))

            assert re.search("Virtual Machines", self.virtual_machines_title.text),  \
                "Running VMs page title is wrong"
            assert self.total_vms_text.text == "0", "Total VMs number is displayed wrong"

            target_textblock = "The VDSM service is not responding on this host"

            assert re.search(target_textblock, self.vdsm_unactived_textblock.text), \
            "The VDSM service is responding on this host"

    def check_vms_in_cluster_unregister(self):
        """
        Purpose:
            Check VMs in cluster (Unregister to RHEVM)
            status in virtual machines page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vms_in_cluster_btn.click()
            self.wait(1)
            try:
                assert self.w.switch_to_alert()
            except NoAlertPresentException as e:
                raise e

    def check_running_vms_register(
        self,
        he_vm_fqdn,
        he_vm_ip,
        he_password,
        second_vm_fqdn):
        """
        Purpose:
            Check running VMs (Register to RHEVM) status
            Suppose this VM is Hosted Engine and another common VM
        """
        # Delete the previous screenshot of the VM page
        with settings(warn_only=True):
            cmd1 = "rm -f /tmp/cockpit_auto/running_vms.png"
            run(cmd1)
            cmd2 = "rm -f /tmp/cockpit_auto/he_vm_detail.png"
            run(cmd2)
            cmd3 = "rm -f /tmp/cockpit_auto/common_vm_detail.png"
            run(cmd3)

        # Screenshot of the VM page
        self.save_screenshot("running_vms.png")

        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))

            # To Do: Need to check the accurate up time
            assert self.vm_up_txts, "VM up time text not exists"

            he_vm_sequence_num = 0
            common_vm_sequence_num = 1
            # Check HostedEngine VM and common vm without any guest OS
            for k, hostname_link in enumerate(list(self.vm_hostname_links)):
                if re.search("HostedEngine", hostname_link.text):
                    if k == 1:
                        common_vm_sequence_num = 0
                    he_vm_sequence_num = k

                    assert re.search(he_vm_ip, list(self.vm_guest_ip_txts)[k].text),    \
                        "HE Guest IP text not correct"
                    assert re.search(he_vm_fqdn, self.vm_hostname_txts[k].text),    \
                        "HE hostname text not correct"
                else:
                    re.search(second_vm_fqdn, list(self.vm_hostname_links)[k].text),     \
                        "Second VM name not correct"

            # Click to check the detail info of the HE vm
            list(self.vm_hostname_links)[he_vm_sequence_num].click()

            self.save_screenshot("he_vm_detail.png")
            assert re.search(
                "HostedEngine", self.name_first_row_second_column.text) # HostedEngine

            assert re.search(
                he_vm_ip, self.ip_first_row_fourth_column.text) # HE vm ip

            cmd = "cat /proc/cpuinfo|grep processor|wc -l"
            with settings(
                warn_only=True,
                host_string='root@' + he_vm_ip,
                password=he_password):
                vcpu_count = run(cmd)
            assert re.search(
                vcpu_count, self.vcpu_second_row_fourth_column.text) # VCPU count

            assert re.search(
                "None", self.username_third_row_second_column.text) # Username
            '''
            assert re.search(
                "vnc", self.display_fourth_row_second_column.text) # Display type
            '''
            assert re.search(
                he_vm_fqdn, self.fqdn_fourth_row_fourth_column.text) # FQDN

            # Click to screenshot the detail of common VM
            list(self.vm_hostname_links)[common_vm_sequence_num].click()
            self.wait(2)
            self.save_screenshot("/tmp/common_vm_detail.png")

    def check_vms_lifecycle(self):
        """
        Purpose:
            Check life-cycle of VMs in virtual machines page
            Suppose this VM is Hosted Engine
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            assert self.vm_lifecycle_btn, "VM lifecycle button not exists"
            assert self.vm_lifecycle_btn.click()

            assert self.vm_lifecycle_operations,    \
                "VM lifecycle operations buttons not exist"

            # TO Do: operation like restart, force off
            pass

    def check_vdsm_elements(self):
        """
        Purpose:
            Check vdsm page elements exist
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            assert self.vdsm_service_management_link,   \
                "The VDSM service management link is missing"
            assert self.vdsm_conf_textarea, \
                "The VDSM config editor is missing"
            assert self.vdsm_save_btn,  \
                "The VDSM config editor save button is missing"
            assert self.vdsm_reload_btn,    \
                "The VDSM config editor reload button is missing"

    def check_vdsm_conf_edit(self):
        """
        Purpose:
            Check vdsm textarea is editable
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            self._edit_vdsm_conf("#some_text")
            assert self.vdsm_conf_textarea.get_attribute('value').endswith("some_text"),    \
                "Edit vdsm.conf textarea failed"
            self.wait(1)
            self._vdsm_conf_confirm(self.vdsm_reload_btn)
            self._vdsm_conf_confirm(self.vdsm_save_btn)
            if not self._check_vdsm_conf_host():
                print "edit operation is successful"

            # TODO: Add VDSM service Management link testing
            pass

    def check_vdsm_conf_save(self):
        """
        Purpose:
            Check save function of vdsm page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            if self.vdsm_save_btn:
                self._check_vdsm_config_dialog(self.vdsm_save_btn)

    def check_vdsm_conf_reload(self):
        """
        Purpose:
            Check reload function of vdsm page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            if self.vdsm_reload_btn:
                self._check_vdsm_config_dialog(self.vdsm_reload_btn)

    def _edit_vdsm_conf(self, input):
        """
        Purpose:
            Append text to vdsm.conf
        """
        self.vdsm_conf_textarea.send_keys(input)

    def _check_vdsm_config_dialog(self, button):
        """
        Purpose:
            Check dialogue in vdsm page
        """
        button.click()
        self.wait(1)
        if button.text == 'Save':
            assert re.search("Save to vdsm.conf", self.vdsm_config_dialog_title.get_attribute('innerHTML')),    \
                "Dialogue is not save to vdsm.conf"
            assert self.vdsm_config_dialog_text.get_attribute('innerHTML').startswith("Content of vdsm.conf file will be replaced."),\
                "Dialogue text is wrong!"
        elif button.text == "Reload":
            assert re.search("Reload stored vdsm.conf", self.vdsm_config_dialog_title.\
                get_attribute('innerHTML')), "Dialogue is not reload stored vdsm.conf"
            assert self.vdsm_config_dialog_text.get_attribute('innerHTML').startswith(\
                "Content of vdsm.conf will be reloaded, unsaved changes will be lost."), "Dialogue text is wrong!"
        assert self.vdsm_config_dialog_ok, "Save button is missing in the dialogue"
        assert self.vdsm_config_dialog_cancel, "Cancel button is missing in the dialogue"

        if self.vdsm_config_dialog_cancel.click():
            self.wait(1)
            print "The function of cancel button in vdsm.conf dialogue is invalid"
            self.wait(1)
        else:
            self.wait(1)
        button.click()
        self.wait(1)
        if self.vdsm_config_dialog_ok.click():
            self.wait(1)
            print "The function of cancel button in vdsm.conf dialogue is invalid"
            self.wait(1)
        else:
            self.wait(1)
            if button.text == 'Save':
                assert re.search("Saved", self.vdsm_config_dialog_saved.text), \
                "Save to vdsm.conf failed"
            elif button.text == 'Reload':
                assert re.search("Loaded", self.vdsm_config_dialog_saved.text), \
                "Load to vdsm.conf failed"
            self.wait(5)
            assert re.search("", self.vdsm_config_dialog_saved.text)

    def _vdsm_conf_confirm(self, button):
        """
        Purpose:
            Confirm dialogue
        """
        button.click()
        self.wait(1)
        self.vdsm_config_dialog_ok.click()
        self.wait(2)

    def _check_vdsm_conf_host(self):
        """
        Purpose:
            Check vdsm config file on remote host
        """
        remote_path = "/etc/vdsm/vdsm.conf"
        fd = StringIO()
        get(remote_path, fd)
        content = fd.getvalue()
        assert not re.search("#some_text", content),   \
            "Edit & Save vdsm.conf failed"

    def check_vm_login_to_engine(self, he, he_password):
        """
        Purpose:
            Check the function to click the login to engine
            Suppose the VM is "HOSTED ENGINE"
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            # Click the engine login link
            self.engine_login_link.click()
            self.wait(1)

            # Input engine login password
            self.engine_login_passwd_input.clear()
            self.wait(1)
            self.engine_login_passwd_input.send_keys(he_password)

            # Input the HE url
            he_url = "https://" + he + "/ovirt-engine"
            self.engine_login_url_input.clear()
            self.wait(1)
            self.engine_login_url_input.send_keys(he_url)

            # Submit to login HE
            self.engine_login_submit_btn.click()
            self.wait(5)

            assert re.search("Logout from Engine", self.engine_login_link.text),    \
                "Failed to login Engine"

    def check_vm_logout_from_engine(self):
        """
        Purpose:
            Check the function to click the login to engine
            Suppose the VM is "HOSTED ENGINE"
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            # Ensure it had been login to engine
            assert re.search("Logout from Engine", self.engine_login_link.text),     \
                "No need to logout from engine"

            # Click the engine login link
            self.engine_login_link.click()
            self.wait(1)

            assert re.search("Login to Engine", self.engine_login_link.text),  \
                "Failed to logout from Engine"

    def check_vm_host_to_maintenance(self):
        """
        Purpose:
            Check Host to Maintenance in virtual machines page
        """
        pass

    def check_vm_refresh(self):
        """
        Purpose:
            Check Refrash in virtual machines page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            print self.refresh_link.text
            if re.search("Refresh: auto", self.refresh_link.text):
                    self.refresh_link.click()
                    self.wait(2)
                    print self.refresh_link.text
                    assert re.search("Refresh: off", self.refresh_link.text),   \
                        "Refresh click not switch to off"
            else:
                self.refresh_link.click()
                self.wait(2)
                print self.refresh_link.text
                assert re.search("Refresh: auto", self.refresh_link.text),    \
                    "Refresh click not switch to auto"

    def logout_from_cockpit(self):
        """
        Purpose:
            Logout from cockpit
        """
        self.content_username_txt.click()
        self.wait(0.5)
        self.logout_link.click()
        self.wait(0.5)
