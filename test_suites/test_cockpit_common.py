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
        :avocado: tags=common_Login_tier1
        """
        self.check_firefox_login()
    
    @add_case_id("RHEVM-23251")
    def test_chrome_login(self):
        """
        :avocado: tags=common_Login_tier1
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
        :avocado: tags=lsy
        """
        self.login_remote_machine()
    
    @add_case_id("RHEVM-23290")
    def test_suscription(self):
        """
        :avocado: tags=abc
        """
        self.subscription_to_rhsm()
    
