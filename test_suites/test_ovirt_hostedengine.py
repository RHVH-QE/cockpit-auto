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
        self.browser.assert_element_visible(self.GETTING_START_LINK)
        self.browser.assert_element_visible(self.MORE_INFORMATION_LINK)

    def test_node_zero_deploy(self):
        a = self.get_data('ovirt_hostedengine.yml')
        config_dict = yaml.load(open(a))
        def prepare_env():
            self.move_failed_setup_log()
            self.install_rhvm_appliance(config_dict['rhvm_appliance_path'])
            self.clean_nfs_storage(
                config_dict['nfs_ip'],
                config_dict['nfs_pass'],
                config_dict['nfs_dir'])

        def check_deploy():
            # VM STAGE
            self.browser.click(self.HE_START)
            self.browser.input_text(self.VM_FQDN, config_dict['he_vm_fqdn'])
            self.browser.input_text(self.MAC_ADDRESS, config_dict['he_vm_mac'])
            self.browser.input_text(self.ROOT_PASS, config_dict['he_vm_pass'])
            self.browser.click(self.NEXT_BUTTON)

            # ENGINE STAGE
            self.browser.input_text(self.ADMIN_PASS, config_dict['admin_pass'])
            self.browser.click(self.NEXT_BUTTON)

            # PREPARE VM
            self.browser.click(self.PREPARE_VM_BUTTON)
            # if self.browser.assert_element_visible(self.FAILED_TEXT, 300):
            #     raise Exception("HostedEngine deployment failed on local VM, please check the logs.")
            # else:
            #     pass
            self.browser.click(self.NEXT_BUTTON, 600)

            # STORAGE STAGE
            self.browser.input_text(self.STORAGE_CONN, config_dict['nfs_ip'] + ':' + config_dict['nfs_dir'])
            self.browser.click(self.NEXT_BUTTON)

            #FINISH STAGE
            # self.browser.click(self.FINISH_DEVELOPMENT)
            # if self.browser.assert_element_visible(self.FAILED_TEXT, 500):
            #     raise Exception("HostedEngine deployment failed on target VM, please check the logs")
            # else:
            #     pass
            self.browser.click(self.CLOSE_BUTTON, 1500)
        prepare_env()
        check_deploy()

    def test_hostedengine_deployed(self):
        if not self.browser.assert_element_visible("XPATH{}//p[contains(text(),'Hosted Engine is running on')]"):
            raise Exception("ERR: HostedEngine is not running on host.")

    def test_maintenance_hint(self):
        if not self.browser.assert_element_visible(self.MAINTENANCE_HINT):
            raise Exception("ERR: NO maintenance hint gived.")

    def test_engine_vm_status(self):
        if not self.browser.assert_element_visible(self.ENGINE_UP_ICON):
            raise Exception("ERR: The engine status is not up, please check.")

    def test_no_password_saved(self):
        a = self.get_data('ovirt_hostedengine.yml')
        config_dict = yaml.load(open(a))
        self.check_no_password_saved(config_dict['he_vm_pass'], config_dict['admin_pass'])

    def test_no_large_messages(self):
        self.check_no_large_messages()

    def test_additional_host(self):
        a = self.get_data('ovirt_hostedengine.yml')
        config_dict = yaml.load(open(a))
        self.add_additional_host_to_cluster(
            config_dict['second_host'],
            config_dict['second_vm_fqdn'],
            config_dict['second_pass'],
            config_dict['he_vm_fqdn'],
            config_dict['admin_pass'])

    def test_local_maintenance(self):
        self.put_host_to_local_maintenance()
        self.browser.assert_text_expected(self.LOCAL_MAINTEN_STAT, 'true')

    def test_migrated_he(self):
        self.browser.assert_text_expected(self.VM_STATUS, 'down')

    def test_remove_maintenance(self):
        self.remove_host_from_maintenance()
        self.browser.assert_text_not_expected(self.LOCAL_MAINTEN_STAT, 'true')

    def test_global_maintenance(self):
        self.put_cluster_to_global_maintenance()
        self.browser.assert_element_visible(self.GLOBAL_HINT)

    def test_hostedengine_redeploy(self):
        """
        :avocado: tags=he
        """
        self.clean_hostengine_env()
        self.test_node_zero_deploy()

        
