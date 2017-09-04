from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.ui_dashboard_page import DashboardPage
from fabric.api import run, env, settings
from cases import CONF
import logging
import const
from utils.helpers import get_cur_func


dict1 = dict(zip(const.common_ui, const.common_ui_id))

log = logging.getLogger("sherry")


host_ip, host_user, host_password, browser, second_ip, second_password = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('common').get(
            'browser'), CONF.get('hosted_engine').get('second_host'), CONF.get(
                'hosted_engine').get('second_password')

env.host_string = host_user + '@' + host_ip
env.password = host_password


def init_browser():
    if browser == 'firefox':
        driver = webdriver.Firefox()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
    elif browser == 'chrome':
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)
        driver.root_uri = "https://{}:9090".format(host_ip)
        return driver
    else:
        raise NotImplementedError


def test_login(ctx):
    log.info("Test common_ui_dashboard-->Trying to login to the browser...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def check_dashboard_cpu(ctx):
    """
    RHEVM-18372
        CPU shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking CPU button...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_cpu()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
       

def check_dashboard_memory(ctx):
    """
    RHEVM-18373
        Memory shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking memory button...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_memory()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_dashboard_network(ctx):
    """
    RHEVM-18374
        Network shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking network button...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_network()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_dashboard_disk_io(ctx):
    """
    RHEVM-18372
        Disk IO shown in cockpit page
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking disk_io button")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_disk_io()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_another_server(ctx):
    """
    RHEVM-18372
        Servers can be added in Dashboard page
    """
    # To do:
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking whether adding the second host...")
        dashboard_page = DashboardPage(ctx)
        dashboard_page.check_server_can_be_added(second_ip, second_password)
    except Exception as e:
        log.info('func_(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func_(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_ui_logs(ctx):
    """
    RHEVM-18394
        Check servers status
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking the logs...")
        log_page = LogPage(ctx)
        log_page.basic_check_elements_exists()
        log.info("Checking the recent logs...")
        log_page.check_recent_logs()
        log.info("Checking the current logs...")
        log_page.check_current_boot_logs()
        log.info("Checking the last 24h logs...")
        log_page.check_last_24hours_logs()
        log.info("Checking the last 7d logs...")
        log_page.check_last_7days_logs()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_ui_services(ctx):
    """
    RHEVM-18392
        Check servers status
    """
    log.info("Checking the services")
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Checking the services")
        service_page = ServicePage(ctx)
        service_page.basic_check_elements_exists()
        log.info("Checking the disable service action...")
        service_name = service_page.disable_service_action()
        service_page.check_service_is_disabled(service_name)
        log.info("Checking the enable service action...")
        service_page.enable_service_action()
        service_page.check_service_is_enabled(service_name)
        log.info("Checking the stop service action...")
        service_page.stop_service_action()
        service_page.check_service_is_stoped(service_name)
        log.info("Checking the start service action...")
        service_page.start_service_action()
        service_page.check_service_is_started(service_name)
        log.info("Checking the restart service action...")
        service_page.restart_service_action()
        service_page.check_service_is_restarted(service_name)
    except AssertionError as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_allowunknown_default(ctx):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is default in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to login into remote machine with 'allowUnknow' is default in cockpit ...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_default()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_allowunknown_true_wrong_account(ctx):
    """
    RHEVM-18381
        Wrong account to login into remote machine
        with "allowUnknow" is true in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Wrong account to login into remote machine with 'allowUnknow' is true in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_wrong_account(second_ip)
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_allowunknown_true_remote_closed(ctx):
    """
    RHEVM-18382
        Login remote closed host with "allowUnknow" is true in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to login remote closed host with 'allowUnknow' is true in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_remote_closed(second_ip, "root", second_password)
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def check_allowunknown_true_wrong_address(ctx):
    """
    RHEVM-18383
        Login remote host with wrong address in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to login remote host with wrong address in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_wrong_address()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_allowunknown_true_empty_username(ctx):
    """
    RHEVM-18384
        Login remote host with wrong address in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to login remote host with wrong address in cockpit...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true_empty_username(second_ip, "root", second_password)
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_allowunknown_true(ctx):
    """
    RHEVM-18380
        Login into remote machine with "allowUnknown" is true in cockpit
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to login into remote machine with 'allowUnknow' is true in cockpit ...")
        login_page = LoginPage(ctx)
        login_page.check_allow_unknown_true(second_ip, "root", second_password)
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_system_login_host(ctx):
    """
    RHEVM-18377
        Login cockpit via Firefox browser
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to login cockpit via Firefox browser...")
        login_page = LoginPage(ctx)
        login_page.basic_check_elements_exists()
        login_page.login_with_incorrect_credential()
        time.sleep(2)
        login_page.login_with_credential(host_user, host_password)
        system_page = SystemPage(ctx)
        system_page.check_login_host(host_ip)
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_system_configure_hostname(ctx):
    """
    RHEVM-18385
        Configure hostname
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to configure hostname...")
        system_page = SystemPage(ctx)
        system_page.configure_hostname()
        system_page.check_configure_hostname()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_system_configure_timezone(ctx):
    """
    RHEVM-18386
        Configure timezone
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to configure timezone...")
        system_page = SystemPage(ctx)
        system_page.configure_timezone()
        system_page.check_configure_timezone()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_system_configure_time(ctx):
    """
    RHEVM-18387
        Configure time manually
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to configure time manually...")
        system_page = SystemPage(ctx)
        system_page.configure_time()
        system_page.check_configure_time()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])

def check_change_system_performance_profile(ctx):
    """
    RHEVM-18390
        Change performance profile
    """
    try:
        log.info('Start to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])
        log.info("Trying to change performance profile...")
        system_page = SystemPage(ctx)
        system_page.change_performance_profile()
        system_page.check_change_performance_profile()
    except Exception as e:
        log.info('func(%s)|| {"RHEVM-%d": "failed"}' % (get_cur_func(),dict1[get_cur_func()]))
        log.error(e)
    else:
        log.info('func(%s)|| {"RHEVM-%d": "passed"}' % (get_cur_func(),dict1[get_cur_func()]))
    finally:
        log.info('Finished to run test cases:["RHEVM-%d"]' % dict1[get_cur_func()])


def runtest():
    ctx = init_browser()
    test_login(ctx)
    check_another_server(ctx)
    check_dashboard_cpu(ctx)
    check_dashboard_memory(ctx)
    check_dashboard_network(ctx)
    check_dashboard_disk_io(ctx)
    ctx.close()
