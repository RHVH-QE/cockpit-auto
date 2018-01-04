# test_tools_subscription
cases = {
    'RHEVM-23290': 'check_register_rhsm',
    'RHEVM-23294': 'check_register_rhsm_org',
    'RHEVM-23295': 'check_register_rhsm'
}

config = {
    'rhn_user': 'QualityAssurance',
    'rhn_password': 'VHVFhPS5TEG8dud9',
    'activation_key': 'rhevh',
    'activation_org': '711497',
    'satellite_ip': '10.73.75.177',
    'satellite_hostname': 'satellite62.lab.eng.pek2.redhat.com',
    'satellite_user': 'admin',
    'satellite_password': 'redhat',
    'ca_path': 'https://10.73.75.177/pub/katello-ca-consumer-satellite62.lab.eng.pek2.redhat.com-1.0-1.noarch.rpm'
}
