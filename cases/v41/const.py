common_ui_dashboard = [
    'check_another_server', 'check_dashboard_cpu', 'check_dashboard_memory',
    'check_dashboard_network', 'check_dashboard_disk_io'
]
common_ui_dashboard_id = [18371, 18372, 18373, 18374, 18375]

common_ui_logs = ['check_ui_logs']
common_ui_logs_id = [18394]

common_ui_services = ['check_ui_services']
common_ui_services_id = [18392]

common_ui_system = [
    'check_allowunknown_default', 'check_allowunknown_true',
    'check_allowunknown_true_wrong_account',
    'check_allowunknown_true_remote_closed',
    'check_allowunknown_true_wrong_address',
    'check_allowunknown_true_empty_username', 'check_system_login_host',
    'check_system_configure_hostname', 'check_system_configure_timezone',
    'check_system_configure_time', 'check_change_system_performance_profile'
]
common_ui_system_id = [
    18379, 18380, 18381, 18382, 18383, 18384, 18377, 18385, 18386, 18387, 18390
]

common_tools_subscription = ['check_subscription_rhsm', 'check_subscription_key', 'check_subscription_password']
common_tools_subscription_id = [18412, 18413, 18414]


dashboard_nodectl = [
    'check_nodectl_help_func', 'check_nodectl_info_func',
    'check_nodectl_check_func', 'check_nodectl_debug_func',
    'check_nodectl_json_func', 'check_nodectl_motd_func',
    'check_nodectl_banner_func'
]
dashboard_nodectl_id = [18545, 18547, 18550, 18551, 18552, 18830, 18831]

dashboard_ui = [
    'check_node_status_func', 'check_node_health_func', 'check_node_info_func',
    'check_network_func', 'check_system_log_func', 'check_storage_func',
    'check_ssh_key_func'
]
dashboard_ui_id = [18534, 18535, 18536, 18540, 18541, 18542, 18543]

dashboard_ui_efi = ['check_nodestatus_efi']
dashboard_ui_efi_id = [18539]

dashboard_ui_fc = ['check_nodestatus_fc']
dashboard_ui_fc_id = [18538]

he_install = ['check_he_install']
he_install_id = [18667]

he_info = [
    'check_engine_status_func', 'check_vm_status_func',
    'check_three_buttons_func', 'check_he_running_on_host_func',
    'check_no_password_saved_func'
]
he_info_id = [18669, 18670, 18671, 18672, 18685]

he_info_add_host = [
    'check_add_additional_host', 'check_put_local_maintenance',
    'check_remove_from_maintenance', 'check_put_global_maintenance'
]
he_info_add_host_id = [18668, 18678, 18679, 18680]

he_install_bond = ['check_he_install_bond']
he_install_bond_id = [18674]

he_install_vlan = ['check_he_install_vlan']
he_install_vlan_id = [18675]

he_install_bv = ['check_he_install_bv']
he_install_bv_id = [18677]

he_install_non_default_port = ['check_he_install_non_default']
he_install_non_default_port_id = [18667]

he_install_redeploy = ['check_he_install_redeploy']
he_install_redeploy_id = [18686]

vm_registerd = [
    'check_running_vms_register_func', 'check_vdsm_func',
    'check_vm_login_logout_engine_func', 'check_vm_refresh_func',
    'check_non_root_alert_func'
]
vm_registerd_id = [18805, 18808, 18809, 18811, 18813]

vm_unregisterd = ['check_running_vms_unregister_func', 'check_vms_in_cluster_unregister_func']
vm_unregisterd_id = [18803, 18804]
