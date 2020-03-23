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
        :avocado: tags=common_tier2
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
    
    @add_case_id("RHEVM-23253")
    def test_login_remote_machine(self):
        """
        :avocado: tags=common_tier1
        """
        self.login_remote_machine()
    
    @add_case_id("RHEVM-23290")
    def test_suscription(self):
        """
        :avocado: tags=common_tier1ab
        """
        self.subscription_to_rhsm()
        self.check_packages_installation()
        #bug
    
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

    @add_case_id("RHEVM-25363")
    def test_udisks_service(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_udisks_service()
    
    @add_case_id("RHEVM-23298")
    def test_check_appliance_like_text(self):
        """
        :avocado: tags=common_tier
        """
        self.check_appliance_like_text()
    
    @add_case_id("RHEVM-24229")
    def test_check_kernel_dump_service(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_service_status()
    
    @add_case_id("RHEVM-23295")
    def test_check_password_is_encrypted(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_password_is_encrypted_in_log()
    
    @add_case_id("RHEVM-24230")
    def test_capture_vmcore_at_local(self):
        """
        :avocado: tags=common_tier1
        """
        self.capture_vmcore_at_local()
    

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
    
    @add_case_id("RHEVM-23256")
    def test_login_wrong_remote_machine(self):
        """
        :avocado: tags=common_tier2
        """
        self.login_wrong_remote_machine()
    
    @add_case_id("RHEVM-23259")
    def test_config_hostname(self):
        """
        :avocado: tags=common_tier2
        """
        self.config_hostname()
    
    @add_case_id("RHEVM-23260")
    def test_config_timezone(self):
        """
        :avocado: tags=common_tier2ab
        """
        self.config_timezone()
        #bug

    @add_case_id("RHEVM-23261")
    def test_config_timezone_manually(self):
        """
        :avocado: tags=common_tier2
        """
        self.config_time_manually()
    
    @add_case_id("RHEVM-23262")
    def test_restart_node(self):
        """
        :avocado: tags=common_tier1
        """
        self.restart_node()
    
    @add_case_id("RHEVM-23264")
    def test_change_performance_profile(self):
        """
        :avocado: tags=common_tier2
        """
        self.change_performance_profile()
    
    @add_case_id("RHEVM-23266")
    def test_check_service_status(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_service_status()
    
    @add_case_id("RHEVM-23270")
    def test_check_file_system_list(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_file_system_list()
    
    @add_case_id("RHEVM-24923")
    def test_modify_nfs_storage(self):
        """
        :avocado: tags=common_tier2
        """
        self.modify_nfs_storage()
        #can not assert progress bar
    
    @add_case_id("RHEVM-23268")
    def test_check_system_logs(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_the_logs()
    
    @add_case_id("RHEVM-23286")
    def test_create_new_account(self):
        """
        :avocado: tags=common_tier2
        """
        self.create_new_account()
    
    @add_case_id("RHEVM-23289")
    def test_check_terminal(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_terminal()

    @add_case_id("RHEVM-23297")
    def test_create_diagnostic_report(self):
        """
        :avocado: tags=common_tier2
        """
        self.create_dignostic_report()
    
    @add_case_id("RHEVM-23300")
    def test_check_selinux_policy(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_selinux_policy()
    
    
    @add_case_id("RHEVM-23294")
    def test_subscription_with_key_and_organization(self):
        """
        :avocado: tags=common_tier2ab
        """
        self.subscription_with_key_and_organization()
        #bug
    
    
    
    
