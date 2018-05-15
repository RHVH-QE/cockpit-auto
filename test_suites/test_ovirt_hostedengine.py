import os
import sys
import yaml
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_ovirt_hostedengine import OvirtHostedEnginePage


class TestOvirtHostedEngine(OvirtHostedEnginePage):
    """
    :avocado: enable
    :avocado: tags=ovirt_hostedengine
    """

    def test_guide_link(self):
        self.check_guide_link()

    def test_node_zero_default_deploy(self):
        # The default deployment means that HE deployment, DHCP network, NFS Auto version, No MNT Option
        """
        :avocado: tags=he_tier1
        """
        self.node_zero_default_deploy_process()

    def test_hostedengine_deployed(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_hostedengine_deployed()

    def test_maintenance_hint(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_maintenance_hint()

    def test_engine_vm_status(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_engine_vm_status()

    def test_no_password_saved(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_no_password_saved_in_setup_log()

    def test_no_large_messages(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_no_large_messages()

    def test_node_zero_iscsi_deployment(self):
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_iscsi_deploy_process()

    def test_node_zero_fc_deployment(self):
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_fc_deploy_process()

    def test_node_zero_gluster_deployment(self):
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_gluster_deploy_process()

    def test_node_zero_static_v4_deploy(self):
        """
        :avocado: tags=he_tier2
        """
        self.node_zero_gluster_deploy_process()

    def test_hostedengine_redeploy(self):
        """
        :avocado: tags=he_tier2
        """
        self.hostedengine_redeploy_process()

    def test_additional_host(self):
        """
        :avocado: tags=he_tier1
        """
        self.add_additional_host_to_cluster_process()

    def test_local_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_local_maintenance()

    def test_migrated_he(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_migrated_he()

    def test_remove_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_remove_maintenance()

    def test_global_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_global_maintenance
