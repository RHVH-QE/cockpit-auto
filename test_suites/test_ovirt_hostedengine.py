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
        self.assert_element_visible(self.GETTING_START_LINK)
        self.assert_element_visible(self.MORE_INFORMATION_LINK)

    def test_node_zero_default_deploy(self):
        # The default deployment means that HE deployment, DHCP network, NFS Auto version, No MNT Option
        """
        :avocado: tags=he_tier1
        """
        a = self.get_data('ovirt_hostedengine.yml')
        config_dict = yaml.load(open(a))

        def prepare_env():
            self.move_failed_setup_log()
            self.install_rhvm_appliance(config_dict['rhvm_appliance_path'])
            self.clean_nfs_storage(config_dict['nfs_ip'],
                                   config_dict['nfs_pass'],
                                   config_dict['nfs_dir'])

        def check_deploy():
            # VM STAGE
            self.click(self.HE_START)
            self.input_text(self.VM_FQDN, config_dict['he_vm_fqdn'])
            self.input_text(self.MAC_ADDRESS, config_dict['he_vm_mac'])
            self.input_text(self.ROOT_PASS, config_dict['he_vm_pass'])
            self.click(self.NEXT_BUTTON)

            # ENGINE STAGE
            self.input_text(self.ADMIN_PASS, config_dict['admin_pass'])
            self.click(self.NEXT_BUTTON)

            # PREPARE VM
            self.click(self.PREPARE_VM_BUTTON)
            self.click(self.NEXT_BUTTON, 1500)

            # STORAGE STAGE
            self.input_text(
                self.STORAGE_CONN,
                config_dict['nfs_ip'] + ':' + config_dict['nfs_dir'])
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        prepare_env()
        check_deploy()

    def test_hostedengine_deployed(self):
        """
        :avocado: tags=he_tier1
        """
        self.assert_element_visible(self.HE_RUNNING)

    def test_maintenance_hint(self):
        """
        :avocado: tags=he_tier1
        """
        self.assert_element_visible(self.MAINTENANCE_HINT)

    def test_engine_vm_status(self):
        """
        :avocado: tags=he_tier1
        """
        self.assert_element_visible(self.ENGINE_UP_ICON)
        self.assert_element_visible(self.HE_RUNNING)

    def test_no_password_saved(self):
        """
        :avocado: tags=he_tier1
        """
        a = self.get_data('ovirt_hostedengine.yml')
        config_dict = yaml.load(open(a))
        self.check_no_password_saved(config_dict['he_vm_pass'],
                                     config_dict['admin_pass'])

    def test_no_large_messages(self):
        """
        :avocado: tags=he_tier1
        """
        self.check_no_large_messages()

    def test_node_zero_static_v4_deploy(self):
        """
        :avocado: tags=he_tier2
        """
        a = self.get_data('ovirt_hostedengine.yml')
        config_dict = yaml.load(open(a))

        def prepare_env():
            self.move_failed_setup_log()
            self.install_rhvm_appliance(config_dict['rhvm_appliance_path'])
            self.clean_nfs_storage(config_dict['nfs_ip'],
                                   config_dict['nfs_pass'],
                                   config_dict['nfs_dir'])

        def check_deploy():
            # VM STAGE
            self.click(self.HE_START)
            self.input_text(self.VM_FQDN, config_dict['he_vm_fqdn'])
            self.input_text(self.MAC_ADDRESS, config_dict['he_vm_mac'])
            self.click(self.NETWORK_DROPDOWN)
            self.click(self.NETWORK_STATIC)
            self.input_text(self.VM_IP, config_dict['he_vm_ip'])
            self.input_text(self.IP_PREFIX, config_dict['he_ip_prefix'])
            self.input_text(self.DNS_SERVER, config_dict['dns_server'])
            self.input_text(self.ROOT_PASS, config_dict['he_vm_pass'])
            self.click(self.NEXT_BUTTON)

            # ENGINE STAGE
            self.input_text(self.ADMIN_PASS, config_dict['admin_pass'])
            self.click(self.NEXT_BUTTON)

            # PREPARE VM
            self.click(self.PREPARE_VM_BUTTON)
            self.click(self.NEXT_BUTTON, 1500)

            # STORAGE STAGE
            self.input_text(
                self.STORAGE_CONN,
                config_dict['nfs_ip'] + ':' + config_dict['nfs_dir'])
            self.click(self.ADVANCED)
            self.click(self.NFS_VER_DROPDOWN)
            self.click(self.NFS_V4)
            self.click(self.NEXT_BUTTON)

            # FINISH STAGE
            self.click(self.FINISH_DEPLOYMENT)
            self.click(self.CLOSE_BUTTON, 1500)

        prepare_env()
        check_deploy()

    def test_hostedengine_redeploy(self):
        """
        :avocado: tags=he_tier2
        """
        self.clean_hostengine_env()
        self.refresh()
        self.switch_to_frame(self.OVIRT_HOSTEDENGINE_FRAME_NAME)
        self.test_node_zero_default_deploy()

    def test_additional_host(self):
        """
        :avocado: tags=he_tier1
        """
        a = self.get_data('ovirt_hostedengine.yml')
        config_dict = yaml.load(open(a))
        self.add_additional_host_to_cluster(
            config_dict['second_host'], config_dict['second_vm_fqdn'],
            config_dict['second_pass'], config_dict['he_vm_fqdn'],
            config_dict['admin_pass'])
        self.check_additional_host_socre(config_dict['second_host'],
                                         config_dict['second_pass'])

    def test_local_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.put_host_to_local_maintenance()
        self.assert_text_in_element(self.LOCAL_MAINTEN_STAT, 'true')

    def test_migrated_he(self):
        """
        :avocado: tags=he_tier1
        """
        self.assert_text_in_element(self.VM_STATUS, 'down')

    def test_remove_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.remove_host_from_maintenance()
        self.assert_text_not_in_element(self.LOCAL_MAINTEN_STAT, 'true')

    def test_global_maintenance(self):
        """
        :avocado: tags=he_tier1
        """
        self.put_cluster_to_global_maintenance()
        self.assert_element_visible(self.GLOBAL_HINT)
