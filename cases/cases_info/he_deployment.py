# test_hosted_engine_deployment
from collections import OrderedDict

cases_t = (
    ('RHEVM-23815', 'check_he_install'),
    ('RHEVM-24594', 'check_he_hint'),
    ('RHEVM-23817', 'check_engine_status'),
    ('RHEVM-23819', 'check_vm_status'),
    ('RHEVM-23832', 'check_no_large_messages'),
    ('RHEVM-23833', 'check_no_password_saved'),
    ('RHEVM-23816', 'check_additional_host'),
    ('RHEVM-23826', 'check_put_local_maintenance'),
    ('RHEVM-23829', 'check_migrate_he'),
    ('RHEVM-23828', 'check_put_global_maintenance'),
    ('RHEVM-23827', 'check_remove_from_maintenance'),
    ('RHEVM-25065', 'check_he_clean'),
    ('RHEVM-23834', 'check_he_redeploy')
)
cases = OrderedDict(cases_t)


config = {
    'rhvm_appliance_path': 'http://10.66.10.22:8090/rhevm-appliance/',
    'storage_type': 'nfs',
    'nfs_ip': '10.66.148.11',
    'nfs_password': 'redhat',
    'he_install_nfs': '/home/jiawu/nfs3',
    'he_data_nfs': '/home/jiawu/nfs4',
    'sd_name': 'heauto-sd',
    'he_vm_mac': '52:54:00:5e:8e:c7',
    'he_vm_fqdn': 'rhevh-hostedengine-vm-04.lab.eng.pek2.redhat.com',
    'he_vm_domain': 'lab.eng.pek2.redhat.com',
    'he_vm_ip': '10.73.73.100',
    'he_vm_password': 'redhat',
    'engine_password': 'password',
    'second_host': '10.73.73.15',
    'second_password': 'redhat',
    'second_vm_fqdn': 'cockpit-vm',
}
