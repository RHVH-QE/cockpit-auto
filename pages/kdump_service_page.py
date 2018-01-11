from utils.page_objects import PageObject, PageElement


class KdumpServicePage(PageObject):
    # frame name
    frame_right_name = "cockpit1:localhost/system/services"

    service_status_select = PageElement(css="#service-unit-action > button:nth-child(2)")
    # Button after click the service_status_select
    start_btn = PageElement(
        css="#service-unit-action > ul:nth-child(3) > li:nth-child(1) > a:nth-child(1)")
    stop_btn = PageElement(
        css="#service-unit-action > ul:nth-child(3) > li:nth-child(2) > a:nth-child(1)")
    restart_btn = PageElement(
        css="#service-unit-action > ul:nth-child(3) > li:nth-child(3) > a:nth-child(1)")
    reload_btn = PageElement(
        css="#service-unit-action > ul:nth-child(3) > li:nth-child(4) > a:nth-child(1)")
    
    enable_disable_select = PageElement(css="#service-file-action > button:nth-child(2)")
    # Button after click the enable_disable_select
    enable_btn = PageElement(
        css="#service-file-action > ul:nth-child(3) > li:nth-child(1) > a:nth-child(1)")
    disable_btn = PageElement(
        css="#service-file-action > ul:nth-child(3) > li:nth-child(3) > a:nth-child(1)")

    def __init__(self, *args, **kwargs):
        super(KdumpServicePage, self).__init__(*args, **kwargs)
        self.get("/system/services#/kdump.service")
        self.wait(5)
