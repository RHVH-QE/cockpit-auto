from utils.page_objects import PageObject, PageElement


class KdumpPage(PageObject):
    # frame name
    frame_right_name = "cockpit1:localhost/kdump"

    kdump_status_btn = PageElement(css="label.btn:nth-child(1) > span:nth-child(2)")
    service_link = PageElement(xpath="//*[@id='app']/div/table/tr[1]/td[2]/div/a/span")
    dump_location_link = PageElement(xpath="//*[@id='app']/div/table/tr[3]/td[2]/a")
    test_config_btn = PageElement(css="button.btn")

    # Elements after click dump_location_link
    location_select = PageElement(css=".dropdown-toggle")
    directory_input = PageElement(id_="kdump-settings-local-directory")
    compression_checkbox = PageElement(id_="kdump-settings-compression")
    cancel_btn = PageElement(css=".cancel")
    apply_btn = PageElement(css="button.btn:nth-child(2)")

    # Elements after click test_config_btn
    crash_system_btn = PageElement(css="button.btn:nth-child(2)")

    def __init__(self, *args, **kwargs):
        super(KdumpPage, self).__init__(*args, **kwargs)
        self.get("/kdump")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.kdump_status_btn, "Kdump status button not exists"
            assert self.service_link.text == "Service is running", \
                "Kdump service is not running"
            assert self.dump_location_link.text == "locally in /var/crash", \
                "Dump location is not default to {}, not /var/crash".format(
                    self.dump_location_link.text)
            assert self.test_config_btn, "Test configuration button not exists"
