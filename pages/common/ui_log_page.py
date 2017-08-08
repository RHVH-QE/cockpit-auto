from utils.page_objects import PageObject, PageElement


class LogPage(PageObject):
    current_day_menu = PageElement(
        xpath=".//*[@id='journal-current-day-menu']/button")
    errors_btn = PageElement(
        xpath=".//*[@id='journal-prio']/button[1]")
    warnnings_btn = PageElement(
        xpath=".//*[@id='journal-prio']/button[2]")
    notices_btn = PageElement(
        xpath=".//*[@id='journal-prio']/button[3]")
    all_btn = PageElement(
        xpath=".//*[@id='journal-prio']/button[4]")

    # Elements after click the current-day-menu
    recent_btn = PageElement(
        xpath=".//*[@id='journal-current-day-menu']/ul/li[1]/a")
    current_boot_btn = PageElement(
        xpath=".//*[@id='journal-current-day-menu']/ul/li[2]/a")
    last_24hours_btn = PageElement(
        xpath=".//*[@id='journal-current-day-menu']/ul/li[3]/a")
    last_7days_btn = PageElement(
        xpath=".//*[@id='journal-current-day-menu']/ul/li[4]/a")

    # frame name
    frame_right_name = "cockpit1:localhost/system/logs"

    def __init__(self, *args, **kwargs):
        super(LogPage, self).__init__(*args, **kwargs)
        self.get("/system/logs")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.current_day_menu, "current day menu button not exists"
            assert self.errors_btn, "errors button not exists"
            assert self.warnnings_btn, "warnning button not exists"
            assert self.notices_btn, "notices button not exists"
            assert self.all_btn, "all button not exists"

    def check_recent_logs(self):
        """
        Purpose:
            Check recent logs including errors, warnnings, notices, all
        """
        with self.switch_to_frame(self.frame_right_name):
            self.errors_btn.click()
            self.save_screenshot("recent_error_logs.png")
            self.wait(3)

            self.warnnings_btn.click()
            self.save_screenshot("recent_warnnings_logs.png")
            self.wait(3)

            self.notices_btn.click()
            self.save_screenshot("recent_notices_logs.png")
            self.wait(3)

            self.all_btn.click()
            self.save_screenshot("recent_all_logs.png")
            self.wait(3)

    def check_current_boot_logs(self):
        """
        Purpose:
            Check current boot logs including errors, warnnings, notices, all
        """
        with self.switch_to_frame(self.frame_right_name):
            self.current_day_menu.click()
            self.wait(3)
            self.current_boot_btn.click()
            self.wait(5)
            self.errors_btn.click()
            self.wait(3)
            self.save_screenshot("current_boot_error_logs.png")

            self.warnnings_btn.click()
            self.wait(3)
            self.save_screenshot("current_boot_warnnings_logs.png")

            self.notices_btn.click()
            self.wait(3)
            self.save_screenshot("current_boot_notices_logs.png")

            self.all_btn.click()
            self.wait(3)
            self.save_screenshot("current_boot_all_logs.png")

    def check_last_24hours_logs(self):
        """
        Purpose:
            Check current boot logs including errors, warnnings, notices, all
        """
        with self.switch_to_frame(self.frame_right_name):
            self.current_day_menu.click()
            self.wait(3)
            self.last_24hours_btn.click()
            self.wait(5)

            self.errors_btn.click()
            self.wait(3)
            self.save_screenshot("last_24_hours_error_logs.png")

            self.warnnings_btn.click()
            self.wait(3)
            self.save_screenshot("last_24_hours_warnnings_logs.png")

            self.notices_btn.click()
            self.wait(3)
            self.save_screenshot("last_24_hours_notices_logs.png")

            self.all_btn.click()
            self.wait(3)
            self.save_screenshot("last_24_hours_all_logs.png")

    def check_last_7days_logs(self):
        """
        Purpose:
            Check current boot logs including errors, warnnings, notices, all
        """
        with self.switch_to_frame(self.frame_right_name):
            self.current_day_menu.click()
            self.wait(3)
            self.last_7days_btn.click()
            self.wait(5)

            self.errors_btn.click()
            self.wait(3)
            self.save_screenshot("last_7days_error_logs.png")

            self.warnnings_btn.click()
            self.wait(3)
            self.save_screenshot("last_7days_warnnings_logs.png")

            self.notices_btn.click()
            self.wait(3)
            self.save_screenshot("last_7days_notices_logs.png")

            self.all_btn.click()
            self.wait(3)
            self.save_screenshot("last_7days_all_logs.png")
