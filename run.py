# !/usr/bin/env python2.7
"""Main function entry.
Usage:
    python run.py [argv]

Options:
    -h,--help                                          Menu
    v41_debug_tier                                     Test v41_debug_tier
    v41_rhvh_tier1                                     Test v41_rhvh_tier1
    v41_rhvh_tier2                                     Test v41_rhvh_tier2
    v41_rhvh_dashboard_uefi                            Test v41_rhvh_dashboard_uefi
    v41_rhvh_dashboard_fc                              Test v41_rhvh_dashboard_fc
    v41_rhvh_he_install_bond                           Test v41_rhvh_he_install_bond
    v41_rhvh_he_install_bv                             Test v41_rhvh_he_install_bv
    v41_rhvh_he_install_vlan                           Test v41_rhvh_he_install_vlan
    v41_rhvh_he_install_non_default_port               Test v41_rhvh_he_install_non_default_port
    v41_rhvh_he_install_redeploy                       Test v41_rhvh_he_install_redeploy
    v41_rhvh_he_info_add_host                          Test v41_rhvh_he_info_add_host
    v41_rhel_tier1v41_rhvh_he_install_redeploy         Test v41_rhel_tier1v41_rhvh_he_install_redeploy
    v41_rhel_tier2                                     Test v41_rhel_tier2
    v41_centos_tier1                                   Test v41_centos_tier1
    v41_centos_tier2                                   Test v41_centos_tier2
    v41_fedora_tier1                                   Test v41_fedora_tier1
    v41_fedora_tier2                                   Test v41_fedora_tier2

Example:
    python run.py v41_debug_tier

"""
import os, sys, time, json, re, smtplib, shutil
from fabric.api import run, local, get, settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import OrderedDict
from cases import CONF
import cases.v41 as v41



"""
class EmailAction(object):
    def __init__(self):
        self.smtp_server = "smtp.corp.redhat.com"

    def send_email(self, from_addr, to_addr, subject, text, attachment):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addr)
        msg['Subject'] = subject

        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        for a in attachment:
            with open(a, 'rb') as f:
                att = MIMEText(f.read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(a))

                msg.attach(att)
        server = smtplib.SMTP(self.smtp_server, 25)
        try:
            server.sendmail(from_addr, to_addr, msg.as_string())
        except Exception as e:
            print e
        finally:
            server.quit()


def _get_host_ip(test_host):
    if re.search('^[0-9]{1,3}\..*', test_host):
        ips = test_host
    else:
        ips = host_ip

    # Wait for the host is ready
    i = 0
    while True:
        if i > 60:
            raise RuntimeError("Error: Host is not ready for testing.")
        with settings(
                warn_only=True, host_string='root@' + ips, password='redhat'):
            output = run("hostnamectl")
        if output.failed:
            time.sleep(10)
            i += 1
            continue
        break
    return ips


def _format_result(file):
    with open(file, 'r') as f:
        r = json.load(f)
    format_ret = {}
    for case in r['report']['tests']:
        ret.update({case['name']: case['outcome']})

    for k, v in ret.items():
        format_k = k.split('::')[1].split('_')[1]
        if not re.search('\d+', format_k):
            continue
        format_ret.update({'RHEVM-' + format_k: v})
    return json.dumps(format_ret)


def _format_result_to_jfile(raw_jfile, test_build, test_profile):
    # Load the result from json file
    with open(raw_jfile, 'r') as f:
        r = json.load(f)

    raw_cases_result = {}
    fail_cases_result = {}
    pass_cases_result = {}
    total_cases_result = {}
    final_result = {}

    for case in r['report']['tests']:
        raw_cases_result.update({cases['name']: case['outcome']})

    for k, v in raw_cases_result.items():
        format_k = k.split('::')[1].split('_')[1]
        if not re.search('\d+', format_k):
            continue
        if v == "passed":
            pass_cases_result.update({'RHEVM-' + format_k: v})
        elif v == "failed":
            pass_cases_result.update({'RHEVM-' + format_k: v})
        total_cases_result.update({'RHEVM-' + format_k: v})

        profile_cases = {test_profile: total_cases_result}

    pass_count = len(pass_cases_result.keys())
    fail_count = len(fail_cases_result.keys())
    total_count = len(total_cases_result.keys())

    final_result = OrderedDict()
    final_result[test_build] = profile_cases
    final_result['sum'] = OrderedDict()
    final_result['sum'][
        'title'] = "4_1_Node_HE_AutoTest_rhvh-4.1-" + test_build.split("-")[4]
    final_result['sum'][
        'log_url'] = "http://127.0.0.1/" + time.strftime("%Y-%m-%d")
    final_result['sum']['total'] = total_count
    final_result['sum']['passed'] = pass_count
    final_result['sum']['failed'] = fail_count
    final_result['sum'][
        'error'] = len(total_cases_result.keys()) - pass_count - fail_count
    final_result['sum']['errorlist'] = list(fail_cases_result.keys())


def download_logfile(host_user, host_ip, host_password="redhat"):
    # Download the relevent log file
    with settings(
            warn_only=True,
            host_string=host_user + '@' + host_ip,
            password=host_password):
        cmd1 = "find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log"
        ret = run(cmd1)
        local("mkdir -p /tmp/log")
        get("%s" % ret, "/tmp/log/")
        get("/var/log/vdsm", "/tmp/log/")
        get("/var/log/ovirt-hosted-engine-ha", "/tmp/log/")


def run_test():
    # Parse variable from json file export by rhvh auto testing platform
    http_json = "/tmp/request.json"
    with open(http_json, 'r') as f:
        r = json.load(f)
    test_host = r["test_host"]
    test_build = r["test_build"]
    profile = r["test_scenario"]

    test_cases = []
    for c in getattr(test_scen, profile)["CASES"]:
        test_cases.append(c)

    # Get the host ip address from the test host
    try:
        host_ip = _get_host_ip(test_host)
    except RuntimeError as e:
        print e
        sys.exit(1)

    # Get config files by rhvh version
    abspath = os.path.abspath(os.path.dirname(__file__))
    if re.search("^ath_v41", profile):
        test_ver = "v41"
    elif re.search("^ath_v40", profile):
        test_ver = "v40"
    else:
        print "Not support currently"
        sys.exit(1)
    conf_file = os.path.join(abspath, "tests", test_ver, "conf.py")

    # Test cases files which will be appended to the 'pytest' command line
    test_files = []
    for each_file in test_cases:
        test_file = os.path.join(abspath, each_file)
        test_files.append(test_file)

    # Make a dir for storing all the test logs
    now1 = time.strftime("%Y-%m-%d")
    now2 = time.strftime("%H-%M-%S")
    now = time.strftime("%H%m%d%H%M%S")

    #download_logfile("root", host_ip)
    #log_dir = "/tmp/log"

    tmp_log_dir = "/tmp/cockpit-auto.logs/" + \
                   now1 + '/' + now2 + '/' + test_build
    if not os.path.exists(tmp_log_dir):
        os.makedirs(tmp_log_dir)
    #shutil.move(log_dir, tmp_log_dir)

    # Modify the variable value in the config file
    variable_dict = {"HOST_IP": host_ip, "TEST_BUILD": test_build}
    _modify_config_file(conf_file, variable_dict)

    # Execute to do the tests
    #tmp_result_jfile = tmp_log_dir + "/result-" + profile + ".json"
    tmp_result_jfile = tmp_log_dir + "/final_results.json"
    tmp_result_hfile = tmp_log_dir + "/result-" + profile + ".html"

    pytest_args = ['-s', '-v']
    for file in test_files:
        pytest_args.append(file)
    pytest_args.append("--json={}".format(tmp_result_jfile))
    pytest_args.append("--html={}".format(tmp_result_hfile))
    #print pytest_args
    pytest.main(pytest_args)

    # After execute the tests, format the result into human-readable
    _format_result_to_jfile(tmp_result_jfile, test_build, profile)

    # Save the screenshot during tests to tmp_log_dir
    has_screenshot = os.path.exists("/tmp/cockpit-screenshot")
    if has_screenshot:
        shutil.move("/tmp/cockpit-screenshot",
                    tmp_log_dir + "/screenshot-" + now)

    download_logfile("root", host_ip)
    log_dir = "/tmp/log"
    # Save all the logs and screenshot to /var/www/html where httpd is already on
    http_logs_dir = "/var/www/html/" + now1 + '/' + now2
    if not os.path.exists(http_logs_dir):
        os.makedirs(http_logs_dir)
    shutil.move(log_dir, tmp_log_dir)
    shutil.move(tmp_log_dir, http_logs_dir)

    # Send email to administrator
    email_subject = "Test Report For Cockpit-ovirt-%s(%s)" % (profile,
                                                              test_build)
    email_from = "yzhao@redhat.com"
    email_to = ["yzhao@redhat.com"]

    # Get local ip for email content
    with settings(warn_only=True):
        local_hostname = local("hostname --fqdn", capture=True)
        local_ip = local(
            "host %s | awk '{print $NF}'" % local_hostname, capture=True)

    email_text = "1. Please see the Test Report at http://%s/%s/%s/%s" % (
        local_ip, now1, now2, test_build)

    email = EmailAction()
    email_attachment = []
    email.send_email(email_from, email_to, email_subject, email_text,
                     email_attachment)
"""

def main():
    if sys.argv[1] == 'h':
        str =  """Main function entry.
    Usage:
        python run.py [argv]

    Options:
        h,help                                          Menu
        v41_debug_tier                                     Test v41_debug_tier
        v41_rhvh_tier1                                     Test v41_rhvh_tier1
        v41_rhvh_tier2                                     Test v41_rhvh_tier2
        v41_rhvh_dashboard_uefi                            Test v41_rhvh_dashboard_uefi
        v41_rhvh_dashboard_fc                              Test v41_rhvh_dashboard_fc
        v41_rhvh_he_install_bond                           Test v41_rhvh_he_install_bond
        v41_rhvh_he_install_bv                             Test v41_rhvh_he_install_bv
        v41_rhvh_he_install_vlan                           Test v41_rhvh_he_install_vlan
        v41_rhvh_he_install_non_default_port               Test v41_rhvh_he_install_non_default_port
        v41_rhvh_he_install_redeploy                       Test v41_rhvh_he_install_redeploy
        v41_rhvh_he_info_add_host                          Test v41_rhvh_he_info_add_host
        v41_rhel_tier1v41_rhvh_he_install_redeploy         Test v41_rhel_tier1v41_rhvh_he_install_redeploy
        v41_rhel_tier2                                     Test v41_rhel_tier2
        v41_centos_tier1                                   Test v41_centos_tier1
        v41_centos_tier2                                   Test v41_centos_tier2
        v41_fedora_tier1                                   Test v41_fedora_tier1
        v41_fedora_tier2                                   Test v41_fedora_tier2

    Example:
        python run.py v41_debug_tier
    """
        print str
    else:
        print "hello"
        tier = sys.argv[1]
        
        from cases import scen
        test_cases = []
        for c in getattr(scen, sys.argv[1])["CASES"]:
            test_cases.append(c)

        test_moudle = []
        for i in test_cases:
            test_moudle.append(i.split('/')[2].split('.')[0])

   
        for j in test_moudle:
            c = getattr(v41, j)
            c.runtest()
        
    

    


    #test_common_tools.runtest()
    #test_common_ui_dashboard.runtest()
    #test_common_ui_logs.runtest()
    #test_common_ui_services.runtest()
    #test_common_ui_system.runtest()
    #test_he_install_auto.runtest()
    #test_he_install.runtest()
    #test_he_info_add_host.runtest()


if __name__ == '__main__':
    main()
