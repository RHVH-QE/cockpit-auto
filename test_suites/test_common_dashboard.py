import os
import sys
import yaml
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_common_dashboard import CommonDashboardPage
from utils.caseid import add_case_id

class TestCommonDashboard(CommonDashboardPage):
    """
    :avocado: enable
    :avocado: tags=common_dashboard
    """

    @add_case_id("RHEVM-23242")
    def test_add_remote_host_from_dashboard(self):
        """
        :avocado: tags=common_dashboard_tier1
        """
        self.add_remote_hosts()