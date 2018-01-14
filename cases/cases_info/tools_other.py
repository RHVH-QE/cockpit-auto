# test_tools_subscription
from collections import OrderedDict


cases_t = (
    ('RHEVM-23286', 'check_new_account'),
    ('RHEVM-23297', 'check_create_diagnostic'),
    ('RHEVM-23300', 'check_selinux_policy'),
    ('RHEVM-24229', 'check_kdump_service'),
    ('RHEVM-23266', 'check_kdump_service')
)
cases = OrderedDict(cases_t)


config = {
    'fullname': 'cockpit',
    'username': 'cockpit',
    'password': 'cockpitauto'
}
