import re
from utils.page_objects import PageObject, PageElement, MultiPageElement


class DashboardUiPage(PageObject):
    """To check Node status and System info on Virtualization panel."""
    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    virtualization_title = PageElement(tag_name='h2')

    node_status_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[1]/tr/td/h4')

    vm_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[2]/div/ul/li/div/div[2]')
    vm_quantity = PageElement(
        xpath='//*[@id="content"]/div/div/div[2]/div/ul/li/div/div[3]/strong')

    health_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[2]/tr[1]/td[1]')
    health_link = PageElement(
        xpath='.//*[@id="content"]/div/div/div[1]/table/tbody[2]/tr[1]/td[2]/div[1]/a/div')
    ok_icons = MultiPageElement(class_name="pficon-ok")

    cur_layer_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[2]/tr[2]/td[1]')
    cur_layer_link = PageElement(
        xpath='.//*[@id="content"]/div/div/div[1]/table/tbody[2]/tr[2]/td[2]/div[1]/a')

    rollback_btn = PageElement(
        xpath='/html/body/div/div/div[2]/div/div/div[1]/table/tbody[2]/tr[2]/td[2]/div[1]/span/button')

    system_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[3]/tr/td/h4')
    
    network_info_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[4]/tr[1]/td[1]')
    network_info_link = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[4]/tr[1]/td[2]/a')
    system_logs_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[4]/tr[2]/td[1]')
    system_logs_link = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[4]/tr[2]/td[2]/a')
    storage_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[4]/tr[3]/td[1]')
    storage_link = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[4]/tr[3]/td[2]/a')
    ssh_key_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[5]/tr/td[1]')
    ssh_key_link = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[5]/tr/td[2]/a')

    # After click health link
    node_health_dialog_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[2]/tr[1]/td[2]/div[2]/div/div/div/div[1]/h4')
    # accordion_header_btn: like "Thin storage","basic storage","Mount points" button
    health_dialog_btns = MultiPageElement(class_name="accordion-header")
    # close_btn : close button,like "X"
    close_btns = MultiPageElement(class_name="close")

    # After click current layer link
    # elements under Node information dialog
    cur_layer_dialog_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[2]/tr[2]/td[2]/div[2]/div/div/div/div[1]/h4')
    layer_dialog_btns = MultiPageElement(class_name='accordion-header')
    entry_txts = MultiPageElement(class_name="col-md-6")

    # Host RSA key title
    ssh_key_dialog_title = PageElement(
        xpath='//*[@id="content"]/div/div/div[1]/table/tbody[5]/tr/td[2]/div/div/div/div/div[1]/h4')

    def __init__(self, *args, **kwargs):
        super(DashboardUiPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            # virtualization title
            assert self.virtualization_title.text == 'Virtualization', \
                "Virtualization Title not correct"
            # node status title 
            assert self.node_status_title.text == "Node Status", \
                "Node Status not correct"
            # vm title and quantity
            assert self.vm_title.text == "Virtual Machines", \
                "Virtual Machines title not correct"
            assert self.vm_quantity, "Vm quantity not exists"
            # health title and status
            assert self.health_title.text == 'Health', \
                "Health title not correct"
            assert re.search('ok', self.health_link.text), "Health is not ok" 
            # current layer title and info
            assert self.cur_layer_title.text == "Current Layer", \
                "Current Layer title not correct"
            assert self.cur_layer_link, "Current layer button not exists"
            # rollback button
            assert self.rollback_btn, "Rollback button not exists"
            # system title and info
            assert self.system_title.text == "System", \
                "System title not correct"
            # network info title and link
            assert re.search('Networking Information', self.network_info_title.text), \
                "Network information title not correct"
            assert self.network_info_link, "Network info link not exists"
            # system logs title and link
            assert re.search("System Logs", self.system_logs_title.text), \
                "System logs title not correct"
            assert self.system_logs_link, "System logs link not exists"
            # storage title and link
            assert re.search("Storage", self.storage_title.text), \
                "Storage title not correct"
            assert self.storage_link, "Storage link not exists"
            # ssh key title and link
            assert re.search("SSH Host Key", self.ssh_key_title.text), \
                "SSH host key title not correct"
            assert self.ssh_key_link, "SSH host key link not exists"
