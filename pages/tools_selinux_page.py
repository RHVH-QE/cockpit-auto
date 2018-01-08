from utils.page_objects import PageObject, PageElement


class SelinuxPage(PageObject):
    # frame name
    frame_right_name = "cockpit1:localhost/selinux/setroubleshoot"

    policy_btn_div = PageElement(css=".btn-group")
    policy_btn = PageElement(css="label.btn:nth-child(2) > span:nth-child(2)")

    def __init__(self, *args, **kwargs):
        super(SelinuxPage, self).__init__(*args, **kwargs)
        self.get("/selinux/setroubleshoot")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.policy_btn_div, "No Selinux policy btn exists"
