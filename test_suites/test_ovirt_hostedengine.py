import os
import sys
import yaml
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_ovirt_hostedengine import OvirtHostedEnginePage
from utils.caseid import add_case_id


class TestOvirtHostedEngine(OvirtHostedEnginePage):
    """
    :avocado: enable
    :avocado: tags=ovirt_he
    """
    @add_case_id("RHEVM-25794")
    def test_guide_link(self):
        """
        :avocado: tags=he_tier1
        """
        self.prepare_env()
        self.assert_element_visible(self.GETTING_START_LINK)
        self.assert_element_visible(self.MORE_INFORMATION_LINK)

    @add_case_id("RHEVM-26339")
    def test_errors_warnings_vm_setting(self):
        # Check the error message and warning message display when setting vm with illegal value.
        """
        :avocado: tags=he_tier1
        """
        self.errors_warnings_vm_setting()

    @add_case_id("RHEVM-26340")
    def test_errors_warnings_engine_setting(self):
        # Check the error message and warning message display when setting engine with illegal value.
        """
        :avocado: tags=he_tier1
        """
        self.errors_warnings_engine_setting()

    @add_case_id("RHEVM-23815")
    def test_node_zero_default_deploy(self):
        # The default deployment means that HE deployment, DHCP network, NFS Auto version, No MNT Option
        """
        :avocado: tags=he_tier1
        """
        self.node_zero_default_deploy_process()

    @add_case_id("RHEVM-26161")
    def test_maintenance_hint(self):
        """
        :avocado: tags=he_tier1
        """
        self.assert_element_visible(self.MAINTENANCE_HINT)

    @add_case_id("RHEVM-26151")
    def test_engine_vm_status(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_hosted_engine_status()

    @add_case_id("RHEVM-23833")
    def test_no_password_saved(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_no_password_saved_in_setup_log()

    @add_case_id("RHEVM-26157")
    def test_no_large_messages(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_no_large_messages()

    @add_case_id("RHEVM-26034")
    def test_base_on_registering_insights_server(self):
        """
        :avocado: tags=he_tier1
        """
        # self.clean_hostengine_env()
        self.deploy_on_registering_insights_server()

    @add_case_id("RHEVM-25065")
    def test_clean_environment(self):
        """
        :avocado: tags=he_tier1
        """
        self.clean_hostengine_env()
        
    @add_case_id("RHEVM-26159")
    def test_hostedengine_redeploy(self):
        # Re-deploy HE on the host
        """
        :avocado: tags=he_tier1
        """
        self.hostedengine_redeploy_process()

    @add_case_id("RHEVM-26150")
    def test_additional_host(self):
        """
        :avocado: tags=he_tier1
        """
        self.add_additional_host_to_cluster_process()

    @add_case_id("RHEVM-26156")
    def test_migrated_he(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_hint_button_before_migration()
        self.check_migrated_he()
        self.check_hint_button_after_migration()

    @add_case_id("RHEVM-26153")
    def test_local_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_local_maintenance()
        self.assert_text_in_element(self.LOCAL_MAINTEN_STAT, 'true')

    @add_case_id("RHEVM-26154")
    def test_remove_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_remove_maintenance()
        self.assert_text_not_in_element(self.LOCAL_MAINTEN_STAT, 'true')

    @add_case_id("RHEVM-26155")
    def test_global_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_global_maintenance()
        self.assert_element_visible(self.GLOBAL_HINT)
        self.check_remove_maintenance()
        self.setting_to_non_default_port()

    @add_case_id("RHEVM-23824")
    def test_non_default_cockpit_port(self):
        # Must run after case "RHEVM-26155 - test_global_maintenance"
        """
        :avocado: tags=he_tier1
        """
        self.deploy_on_non_default_cockpit_port()
        self.setting_to_default_port()

    @add_case_id("RHEVM-26152")
    def test_reboot_hosted_engine_env(self):
        """
        :avocado: tags=he_tier1
        """
        self.clean_hostengine_env()
        self.node_zero_default_deploy_process()
        self.reboot_hosted_engine_env()
        self.check_hosted_engine_status()

    @add_case_id("RHEVM-26160")
    def test_roll_back_history_text(self):
        """
        :avocado: tags=he_tier1
        """
        self.clean_hostengine_env()
        self.node_zero_rollback_deploy_process()

    @add_case_id("RHEVM-25122")
    def test_node_zero_iscsi_deployment(self):
        # Need to deploy HE on iscsi storage
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_iscsi_deploy_process()

    @add_case_id("RHEVM-25010")
    def test_node_zero_fc_deployment(self):
        # Need to deploy HE on FC Storage
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_fc_deploy_process()

    @add_case_id("RHEVM-25793")
    def test_node_zero_gluster_deployment(self):
        # Need to deploy HE on gluster storage
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_gluster_deploy_process()

    @add_case_id("RHEVM-25350")
    def test_node_zero_static_v4_deploy(self):
        # Need to deploy HE with static ip
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_static_v4_deploy_process()

    @add_case_id("RHEVM-26334")
    def test_migrate_normal_host(self):
        """
        :avocado: tags=he_tier
        """
        # self.add_normal_host_to_cluster_process()
        self.assertEqual(self.check_migrated_normal_host(), True)