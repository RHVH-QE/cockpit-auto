from collections import OrderedDict
# test_tools_subscription
'''
cases = OrderedDict([
    ('RHEVM-23286', 'check_new_account'),
    ('RHEVM-23297', 'check_create_diagnostic'),
    ('RHEVM-23300', 'check_selinux_policy'),
    ('RHEVM-24230', 'check_vmcore_local'),
])
'''
cases = OrderedDict([
    ('RHEVM-23297', 'check_create_diagnostic')
])

config = {
    'fullname': 'cockpit',
    'username': 'cockpit',
    'password': 'cockpitauto'
}
