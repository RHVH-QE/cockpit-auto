import re
from utils.page_objects import PageObject, PageElement


class DiagnosticPage(PageObject):
    create_report_btn = PageElement(class_name="btn-primary")

    # Elements after click the create_report_btn
    sos_cancel_btn = PageElement(id_="sos-cancel")
    download_done_div = PageElement(
        xpath=".//*[@id='sos-download']/center/div")
    download_sos_btn = PageElement(
        xpath=".//*[@id='sos-download']/center/button")

    # frame name
    frame_right_name = "cockpit1:localhost/sosreport"

    def __init__(self, *args, **kwargs):
        super(DiagnosticPage, self).__init__(*args, **kwargs)
        self.get("/sosreport")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.create_report_btn, "No create report btn exists"

    def create_sos_report(self):
        """
        Purpose:
            Create the diagnostic report
        """
        with self.switch_to_frame(self.frame_right_name):
            self.create_report_btn.click()

    def check_sosreport_can_be_downloaded(self):
        """
        Purpose:
            Check the sosreport can be downloaded
        """
        with self.switch_to_frame(self.frame_right_name):
            assert self.download_done_div, "sosreport is not created successfully"
            assert re.search("Done", self.download_done_div.text),   \
                "sosreport is not created successfully"
            assert self.download_sos_btn, "sosreport can not be downloaded"
            assert re.search("Download", self.download_sos_btn.text),    \
                "sosreport can not be downloaded"
