v41_debug_tier = {
    "TAG": ["RHVH41"],
    "CASES": [
        "cases/v41/test_dashboard_nodectl.py"
    ]
}

#
# RHVH4.1 test scenario contains multiple cases
#
v41_rhvh_tier1 = {
    "TAG": ["RHVH41"],
    "CASES": [
        "cases/v41/test_dashboard_nodectl.py",
        "cases/v41/test_dashboard_ui.py",
        "cases/v41/test_vm_unregisterd.py",
        "cases/v41/test_common_tools_subscription.py",
        "cases/v41/test_he_install.py",
        "cases/v41/test_he_info.py",
        "cases/v41/test_vm_registerd.py"
    ]
}

v41_rhvh_tier2 = {
    "TAG": ["RHVH41"],
    "CASES": [
        "cases/v41/test_common_ui.py",
        "cases/v41/test_common_tools.py"
    ]
}

#
# RHVH4.1 special machine test scenarios
#

v41_rhvh_dashboard_uefi = {
    "TAG": ["RHVH41"],
    "CASES": ["cases/v41/test_dashboard_ui_efi.py"]
}

v41_rhvh_dashboard_fc = {
    "TAG": ["RHVH41"],
    "CASES": ["cases/v41/test_dashboard_ui_fc.py"],
}

v41_rhvh_he_install_bond = {
    "TAG": ["RHVH41"],
    "CASES": ["cases/v41/test_he_install_bond.py"]
}

v41_rhvh_he_install_bv = {
    "TAG": ["RHVH41"],
    "CASES": ["cases/v41/test_he_install_bv.py"]
}

v41_rhvh_he_install_vlan = {
    "TAG": ["RHVH41"],
    "CASES": ["cases/v41/test_he_install_vlan.py"]
}

v41_rhvh_he_install_non_default_port = {
    "TAG": ["RHVH41"],
    "CASES": ["cases/v41/test_he_install_non_default_port.py"]
}

v41_rhvh_he_install_redeploy = {
    "TAG": ["RHVH41"],
    "CASES": [
        "cases/v41/test_he_install.py", 
        "cases/v41/test_he_install_redeploy.py"
    ]
}

v41_rhvh_he_info_add_host = {
    "TAG": ["RHVH41", "ANOTHER_HOST"],
    "CASES": [
        "cases/v41/test_he_install.py", 
        "cases/v41/test_he_info_add_host.py"]
}

#
# RHEL73 version 4.1 test scenario
#
v41_rhel_tier1 = {
    "TAG": ["RHEL73"],
    "CASES": [
        "cases/v41/test_vm_unregisterd.py",
        "cases/v41/test_common_tools_subscription.py",
        "cases/v41/test_he_install.py", 
        "tests/v41/test_he_info.py",
        "cases/v41/test_vm_registerd.py"
    ]
}

v41_rhel_tier2 = {
    "TAG": ["RHEL73"],
    "CASES": [
        "cases/v41/test_common_ui.py",
        "cases/v41/test_common_tools.py"
    ]
}

#
# CENTOS73 version4.1 test scenarios
#
v41_centos_tier1 = {
    "TAG": ["CENTOS73"],
    "CASES": [
        "cases/v41/test_vm_unregisterd.py",
        "cases/v41/test_common_tools_subscription.py",
        "cases/v41/test_he_install.py", 
        "tests/v41/test_he_info.py",
        "cases/v41/test_vm_registerd.py"
    ]
}

v41_centos_tier2 = {
    "TAG": ["CENTOS73"],
    "CASES": [
        "cases/v41/test_common_ui.py",
        "cases/v41/test_common_tools.py"
    ]
}

v41_fedora_tier1 = {
    "TAG": ["FEDORA24"],
    "CASES": [
        "cases/v41/test_vm_unregisterd.py",
        "cases/v41/test_common_tools_subscription.py",
        "cases/v41/test_he_install.py", 
        "tests/v41/test_he_info.py",
        "cases/v41/test_vm_registerd.py"
    ]
}

v41_fedora_tier2 = {
    "TAG": ["FEDORA24"],
    "CASES": [
        "cases/v41/test_common_ui.py",
        "cases/v41/test_common_tools.py"
    ]
}

v41_gluster_deploy = {
    "TAG": ["gluster"],
    "CASES": [
        "cases/v41/test_deploy_he_over_gluster.py"
    ]
}
