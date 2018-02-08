# test_tools_subscription
from collections import OrderedDict
cases_t = (
    ('RHEVM-23290', 'check_register_rhsm'),
    ('RHEVM-23294', 'check_register_rhsm_org'),
    ('RHEVM-23295', 'check_register_rhsm'),
    ('RHEVM-23296', 'check_register_satellite'),
    ('RHEVM-24721', 'check_register_satellite57')
)
cases = OrderedDict(cases_t)


config = {
    'subscription_url': '***',	
    'rhn_user': '***',
    'rhn_password': '***',
    'activation_key': 'rhevh',
    'activation_org': '711497',
    'satellite_ip': '10.73.75.177',
    'satellite_user': 'admin',
    'satellite_password': 'redhat',
    'satellite57_ip': '10.73.75.178',
    'satellite57_user': 'admin',
    'satellite57_password': 'redhat'
}
