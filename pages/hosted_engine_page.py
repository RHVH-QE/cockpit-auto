import re
from fabric.api import run, env, settings
from utils.rhvmapi import RhevmAction
from utils.page_objects import PageObject, PageElement, MultiPageElement


class HePage(PageObject):
    """
    Hosted engine page
    """
    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    deploy_icon = PageElement(class_name="btn-primary")
    mac_address = PageElement(
        xpath="//input[@title='Enter the MAC address for the VM.']")
    engine_hostname = PageElement(
        xpath="//input[@placeholder='Engine VM Host Name']")
    domain_name = PageElement(
        xpath="//input[@placeholder='Engine VM Domain']")
    passwd = MultiPageElement(
        xpath="//input[@type='password']")
    nfs_path = PageElement(
        xpath="//input[@placeholder='host:/path']")
    next_button = PageElement(
        xpath="//button[@class='btn btn-primary wizard-pf-next']")
    deploy_button = PageElement(
        xpath="//button[@class='btn btn-primary wizard-pf-finish']")
    checkboxes = MultiPageElement(xpath="//input[@type='checkbox']")
    default_button = MultiPageElement(xpath="//button[@class='btn btn-default']")

    alert_warning_maintenance = MultiPageElement(xpath="//div[@class='alert alert-warning']")

    ok_icons = MultiPageElement(class_name="pficon-ok")
    vcenters = MultiPageElement(class_name="vcenter")
    btns = MultiPageElement(class_name="btn-default")
    panel_titles = MultiPageElement(class_name="panel-title")
    panel_bodys = MultiPageElement(class_name="panel-body")

    vm_state_txts = MultiPageElement(
        xpath=".//*[@class='list-view-pf-additional-info']/div/div")
    list_group_item_txts = MultiPageElement(class_name="list-group-item-text")

    #global_maintenance_div = PageElement(xpath=".//*[@class='panel-body']/div")
    global_maintenance_div = PageElement(class_name="alert-warning")


    def __init__(self, *args, **kwargs):
        super(HePage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard#/he")
        self.wait(10)

    def check_three_buttons(self):
        """
        Purpose:
            Chech three "Maintenance" buttons exist
        """
        assert len(list(self.btns)) == 3, "Maintenance buttons not exist"

    def check_local_maintenance_hint(self):
        """
        Purpose:
            Check the local maintenance on one host hint
        """
        assert self.alert_warning_maintenance[0].text == 'Local maintenance cannot be enabled with a single host',   \
            "There is no hint about putting the HostedEngine into local maintenance on one host"

    def check_engine_status(self):
        """
        Purpose:
            Check the engine status
        """
        with self.switch_to_frame(self.frame_right_name):
            ok_icons = list(self.ok_icons)
            assert len(ok_icons) == 2, "Hosted engine status not up"

            he_status_txt = list(self.vcenters)[0]
            assert he_status_txt.text.strip() == "Hosted Engine is up!",    \
                "Hosted engine status not up"

    def check_vm_status(self):
        """
        Purpose:
            Check the host status
        """
        with self.switch_to_frame(self.frame_right_name):
            assert re.search('up', list(self.vm_state_txts)[0].text),   \
                "The VM is not up"

    def check_vm_on_additional_host(self):
        """
        Purpose:
            Check vm on the additional host
        """
        with self.switch_to_frame(self.frame_right_name):
            assert re.search('up', list(self.vm_state_txts)[1].text),   \
                "The VM is not up on the additional host"

    def check_he_running_on_host(self, host_name):
        """
        Purpose:
            Check the hosted engine is running on local host
        """
        with self.switch_to_frame(self.frame_right_name):
            he_running_on_txt = list(self.vcenters)[1]
            assert re.search(host_name, he_running_on_txt.text),     \
                "Hosted engine running on host not correct"

    def put_host_to_local_maintenance(self):
        """
        Purpose:
            Put the host to local maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            put_host_local_maintenace_btn = list(self.btns)[0]
            put_host_local_maintenace_btn.click()
            self.wait(150)

    def check_host_in_local_maintenance(self):
        """
        Purpose:
            Check the host is in local maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            host_agent_maintenance_txt = list(self.list_group_item_txts)[0].text
            host_maintenance_txt = host_agent_maintenance_txt.split()[-1]
            assert host_maintenance_txt == "true",  \
                "Host is not in local maintenance"

    def check_host_not_in_local_maintenance(self):
        """
        Purpose:
            Check the host is not in local maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            host_agent_maintenance_txt = list(self.list_group_item_txts)[0].text
            host_maintenance_txt = host_agent_maintenance_txt.split()[-1]
            assert host_maintenance_txt == "false",     \
                "Host is in local maintenance"

    def remove_host_from_local_maintenance(self):
        """
        Purpose:
            Remove the host from local maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            remove_host_local_maintenace_btn = list(self.btns)[1]
            remove_host_local_maintenace_btn.click()
            self.wait(60)

    def put_cluster_to_global_maintenance(self):
        """
        Purpose:
            Put the cluster to global maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            put_host_local_maintenace_btn = list(self.btns)[2]
            put_host_local_maintenace_btn.click()
            self.wait(10)

    def check_cluster_in_global_maintenance(self):
        """
        Purpose:
            Check whether the cluster is in global maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            assert self.global_maintenance_div, "The cluster is not in global maintenance"
            #if not self.global_maintenance_div.find(True):
            #    assert 0, "The cluster is not in global maintenance"

    def check_cluster_not_in_global_maintenance(self):
        """
        Purpose:
            Check the cluster is not in global maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            assert not self.global_maintenance_div, "The cluster is in global maintenance"

    def check_vm_migrated(self):
        """
            Suppose there are only two hosts,
            check the HE vm already migrate to another host
        """
        with self.switch_to_frame(self.frame_right_name):
            vm_state_txt = list(self.vm_state_txts)[1].text
            vm_status = vm_state_txt.split()[-1]
            assert vm_status == "up",  \
                "The HE vm did not migrated to another host"
            #host_agent_maintenance_txt = list(self.list_group_item_txts)[1].text
            #host_maintenance_txt = host_agent_maintenance_txt.split()[-1]
            #assert host_maintenance_txt == "true",  \
            #    "The HE vm did not migrated to another host"
