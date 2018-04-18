import os
import time
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
            self.browser.input_text(self.CONFIRM_ROOT_PASS, config_dict['he_vm_pass'])
            self.browser.click(self.NEXT_BUTTON)

            # ENGINE STAGE
            self.browser.input_text(self.ADMIN_PASS, config_dict['admin_pass'])
            self.browser.input_text(self.CONFIRM_ADMIN_PASS, config_dict['admin_pass'])
            self.browser.click(self.NEXT_BUTTON)

            # PREPARE VM
            self.browser.click(self.PREPARE_VM_BUTTON)
            self.browser.click(self.NEXT_BUTTON, 2000)
            if self.browser.assert_element_visible(self.REDEPLOY_BUTTON):
                raise Exception("HostedEngine deployment failed on local VM, please check the logs.")

            # STORAGE STAGE
            self.browser.input_text(self.STORAGE_CONN, config_dict['nfs_ip'] + ':' + config_dict['nfs_dir'])
            self.browser.click(self.NEXT_BUTTON)

            #FINISH STAGE
            self.browser.click(self.FINISH_DEVELOPMENT)
            self.browser.click(self.CLOSE_BUTTON, 2000)
            if self.browser.assert_element_visible(self.REDEPLOY_BUTTON):
                raise Exception("HostedEngine deployment failed on target VM, please check the logs")
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
        local_mainten_stat = "XPATH{}//div[@class='list-group-item-text']"
        # self.browser.assert_element_visible(local_mainten)
        self.put_host_to_local_maintenance()
        time.sleep(120)
        self.browser.assert_text_expected(local_mainten_stat, 'true')

    def test_migrated_he(self):
        vm_status = "XPATH{}//div[contains(@class, 'list-view-pf-additional-info-item')]/div"
        self.browser.assert_text_expected(vm_status, 'down')

    def test_remove_maintenance(self):
        local_mainten_stat = "XPATH{}//div[@class='list-group-item-text']"
        self.remove_host_from_maintenance()
        time.sleep(30)
        self.browser.assert_text_not_expected(local_mainten_stat, 'true')

    def test_global_maintenance(self):
        self.put_cluster_to_global_maintenance()
        self.browser.assert_element_visible(self.GLOBAL_HINT)

    def test_hostedengine_redeploy(self):
        pass
