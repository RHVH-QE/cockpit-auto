import logging
from pages.dashboard_ui_page import DashboardUiPage
from cases.helpers import CheckBase


log = logging.getLogger('sherry')


class TestDashboardUi(CheckBase):

    page = None

    def set_page(self):
        self.page = DashboardUiPage(self._driver)

    def check_node_status(self):
        """
        Purpose:
            Check node status in virtualization dashboard
        """
        log.info('Checking node status in virtualization dashboard...')
        try:
            self.page.basic_check_elements_exists()
        except AssertionError as e:
            log.error(e)
            return False
        return True
