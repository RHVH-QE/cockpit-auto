import re
from utils.helpers import RhevmAction
from utils.page_objects import PageObject, PageElement, MultiPageElement
from fabric.api import run, env, settings


class HePage(PageObject):
    """
    Hosted engine page
    """
    ok_icons = MultiPageElement(class_name="pficon-ok")
    vcenters = MultiPageElement(class_name="vcenter")
    btns = MultiPageElement(class_name="btn-default")
    panel_titles = MultiPageElement(class_name="panel-title")
    panel_bodys = MultiPageElement(class_name="panel-body")

    vm_state_txts = MultiPageElement(
        xpath=".//*[@class='list-view-pf-additional-info']/div/div")
    list_group_item_txts = MultiPageElement(class_name="list-group-item-text")

    global_maintenance_div = PageElement(xpath=".//*[@class='panel-body']/div")

    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(HePage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard#/he")
        self.wait(10)

    def check_three_buttons(self):
        """
        Purpose:
            Chech three "Maintenance" buttons exist
        """
        assert len(list(self.btns)) == 2, "Maintenance buttons not exist"

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

    def check_he_running_on_host(self, host_ip):
        """
        Purpose:
            Check the hosted engine is running on local host
        """
        cmd = "hostname"
        hostname = run(cmd)
        with self.switch_to_frame(self.frame_right_name):
            he_running_on_txt = list(self.vcenters)[1]
            print he_running_on_txt.text
            print hostname
            assert re.search(hostname, he_running_on_txt.text),     \
                "Hosted engine running on host not correct"

    def put_host_to_local_maintenance(self):
        """
        Purpose:
            Put the host to local maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            put_host_local_maintenace_btn = list(self.btns)[0]
            put_host_local_maintenace_btn.click()
            self.wait(60)

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
            if not self.global_maintenance_div.find(True):
                assert 0, "The cluster is not in global maintenance"

    def check_vm_migrated(self):
        """
            Suppose there are only two hosts,
            check the HE vm already migrate to another host
        """
        with self.switch_to_frame(self.frame_right_name):
            host_agent_maintenance_txt = list(self.list_group_item_txts)[1].text
            host_maintenance_txt = host_agent_maintenance_txt.split()[-1]
            assert host_maintenance_txt == "true",  \
                "The HE vm did not migrated to another host"
