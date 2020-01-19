import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_common import CommonPages
from utils.caseid import add_case_id

class TestCockpitCommon(CommonPages):
    """
    :avocado: enable
    :avocado: tags=cockpit_common
    """
    @add_case_id("RHEVM-23250")
    def test_firefox_login(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_firefox_login()
    
    @add_case_id("RHEVM-23251")
    def test_chrome_login(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_chrome_login()
    
    @add_case_id("RHEVM-23242")
    def test_add_remote_host(self):
        """
        :avocado: tags=common_tier1
        """
        self.add_remote_host()
    
    @add_case_id("RHEVM-23245")
    def test_delete_remote_host(self):
        """
        :avocado: tags=common_tier1
        """
        self.delete_remote_host()
    
    @add_case_id("RHVEM-23253")
    def test_login_remote_machine(self):
        """
        :avocado: tags=common_tier1
        """
        self.login_remote_machine()
    
    @add_case_id("RHEVM-23290")
    def test_suscription(self):
        """
        :avocado: tags=unfinished
        """
        self.subscription_to_rhsm()
    
    @add_case_id("RHEVM-24922")
    def test_add_nfs_storage(self):
        """
        :avocado: tags=common_tier1
        """
        self.add_nfs_storage()
    
    @add_case_id("RHEVM-23247")
    def test_system_dynamic_status(self):
        """
        :avocado: tags=common_tier1
        """
        self.system__dynamic_status()


    @add_case_id("RHEVM-23243")
    def test_add_remote_host_chrome(self):
        """
        :avocado: tags=common_tier2
        """
        self.add_remote_host()
    
    @add_case_id("RHEVM-23246")
    def test_delete_remote_host_chrome(self):
        """
        :avocado: tags=common_tier2
        """
        self.delete_remote_host()
    
    @add_case_id("RHEVM-23248")
    def test_system_dynamic_status_chrome(self):
        """
        :avocado: tags=common_tier2
        """
        self.system__dynamic_status()
    
    @add_case_id("RHVEM-23256")
    def test_login_wrong_remote_machine(self):
        """
        :avocado: tags=common_tier2
        """
        self.login_wrong_remote_machine()
    
    @add_case_id("RHVEM-23259")
    def test_config_hostname(self):
        """
        :avocado: tags=common_tier2
        """
        self.config_hostname()
    
    @add_case_id("RHVEM-23260")
    def test_config_timezone(self):
        """
        :avocado: tags=common_tier2
        """
        self.config_timezone()

    @add_case_id("RHVEM-23261")
    def test_config_timezone_manually(self):
        """
        :avocado: tags=common_tier2
        """
        self.config_time_manually()
    
    @add_case_id("RHVEM-23262")
    def test_restart_node(self):
        """
        :avocado: tags=common_tier2
        """
        self.restart_node()
    
    @add_case_id("RHVEM-23264")
    def test_change_performance_profile(self):
        """
        :avocado: tags=common_tier2
        """
        self.change_performance_profile()
    
    # @add_case_id("RHVEM-23266")
    # def test_check_service_status(self):
    #     """
    #     :avocado: tags=common_tier2a
    #     """
    #     self.check_service_status()
