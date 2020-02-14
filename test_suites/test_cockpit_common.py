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
    
    @add_case_id("RHVEM-23253")
    def test_login_remote_machine(self):
        """
        :avocado: tags=common_tier1
        """
        self.login_remote_machine()
    
    @add_case_id("RHEVM-23290")
    def test_suscription(self):
        """
        :avocado: tags=common_tier1
        """
        self.subscription_to_rhsm()
        self.check_packages_installation()
    
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
    
    @add_case_id("RHVEM-23298")
    def test_check_appliance_like_text(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_appliance_like_text()
    
    @add_case_id("RHVEM-24229")
    def test_check_kernel_dump_service(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_kernel_dump_service()
    
    add_case_id("RHVEM-23295")
    def test_check_password_is_encrypted(self):
        """
        :avocado: tags=common_tier1
        """
        self.check_password_is_encrypted_in_log()

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
        :avocado: tags=common_tier1
        """
        self.restart_node()
    
    @add_case_id("RHVEM-23264")
    def test_change_performance_profile(self):
        """
        :avocado: tags=common_tier2
        """
        self.change_performance_profile()
    
    @add_case_id("RHVEM-23266")
    def test_check_service_status(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_service_status()
    
    @add_case_id("RHVEM-23270")
    def test_check_file_system_list(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_file_system_list()
    
    @add_case_id("RHVEM-24923")
    def test_modify_nfs_storage(self):
        """
        :avocado: tags=common_tier2
        """
        self.modify_nfs_storage()
    
    @add_case_id("RHVEM-23268")
    def test_check_system_logs(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_the_logs()
    
    @add_case_id("RHVEM-23286")
    def test_create_new_account(self):
        """
        :avocado: tags=common_tier2
        """
        self.create_new_account()
    
    @add_case_id("RHVEM-23289")
    def test_check_terminal(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_terminal()

    # @add_case_id("RHVEM-23317")
    # def test_go_to_network_page(self):
    #     """
    #     :avocado: tags=common_tier2a
    #     """
    #     self.go_to_network_page()
    
    # @add_case_id("RHVEM-23318")
    # def test_go_to_logs_page(self):
    #     """
    #     :avocado: tags=common_tier2a
    #     """
    #     self.go_to_logs_page()
    
    # @add_case_id("RHVEM-23319")
    # def test_go_to_storage_page(self):
    #     """
    #     :avocado: tags=common_tier2a
    #     """
    #     self.go_to_storage_page()

    @add_case_id("RHVEM-23297")
    def test_create_diagnostic_report(self):
        """
        :avocado: tags=common_tier2
        """
        self.create_dignostic_report()
    
    @add_case_id("RHVEM-23300")
    def test_check_selinux_policy(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_selinux_policy()
    
    @add_case_id("RHVEM-23324")
    def test_show_image_information_in_terminal(self):
        """
        :avocado: tags=common_tier2
        """
        self.show_information_in_terminal()
    
    @add_case_id("RHVEM-23327")
    def test_show_system_status_in_terminal(self):
        """
        :avocado: tags=common_tier2
        """
        self.show_system_status_in_terminal()
    
    @add_case_id("RHVEM-23328")
    def test_check_debug_command_in_terminal(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_debug_command_in_terminal()

    @add_case_id("RHVEM-23330")
    def test_check_motd_command_in_terminal(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_motd_command_in_terminal()
    
    @add_case_id("RHVEM-23331")
    def test_check_generate_banner_command_in_terminal(self):
        """
        :avocado: tags=common_tier2
        """
        self.check_generate_banner_command_in_terminal()
    
    
    
    
