from utils.page_objects import PageObject, PageElement


class DiagnosticPage(PageObject):
    # frame name
    frame_right_name = "cockpit1:localhost/sosreport"

    create_report_btn = PageElement(css="button.btn:nth-child(4)")

    # Elements after click the create_report_btn
    sos_cancel_btn = PageElement(id_="sos-cancel")
    download_done_div = PageElement(
        xpath=".//*[@id='sos-download']/center/div")
    download_sos_btn = PageElement(
        xpath=".//*[@id='sos-download']/center/button")

    def __init__(self, *args, **kwargs):
        super(DiagnosticPage, self).__init__(*args, **kwargs)
        self.get("/sosreport")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.create_report_btn, "No create report btn exists"
