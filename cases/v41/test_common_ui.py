from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.ui_dashboard_page import DashboardPage
from pages.v41.ui_service_page import ServicePage
from pages.v41.ui_system_page import SystemPage
from pages.v41.ui_log_page import LogPage
from fabric.api import run, env, settings
from cases import CONF
import time
import logging
import const
from utils.helpers import checkpoint


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


@checkpoint(dict1)
def check_dashboard_cpu(ctx):
    """
    RHEVM-18372
        CPU shown in cockpit page
    """
    log.info("Checking CPU button...")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_cpu()
  

@checkpoint(dict1)
def check_dashboard_memory(ctx):
    """
    RHEVM-18373
        Memory shown in cockpit page
    """
    log.info("Checking memory button...")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_memory()


@checkpoint(dict1)
def check_dashboard_network(ctx):
    """
    RHEVM-18374
        Network shown in cockpit page
    """
    log.info("Checking network button...")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_network()


@checkpoint(dict1)
def check_dashboard_disk_io(ctx):
    """
    RHEVM-18372
        Disk IO shown in cockpit page
    """
    log.info("Checking disk_io button")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_disk_io()


@checkpoint(dict1)
def check_another_server(ctx):
    """
    RHEVM-18372
        Servers can be added in Dashboard page
    """
    log.info("Checking whether adding the second host...")
    dashboard_page = DashboardPage(ctx)
    dashboard_page.check_server_can_be_added(second_ip, second_password)


@checkpoint(dict1)
def check_ui_logs(ctx):
    """
    RHEVM-18394
        Check servers status
    """
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


@checkpoint(dict1)
def check_ui_services(ctx):
    """
    RHEVM-18392
        Check servers status
    """
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


@checkpoint(dict1)
def check_allowunknown_default(ctx):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is default in cockpit
    """
    log.info("Trying to login into remote machine with 'allowUnknow' is default in cockpit ...")
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_default()


@checkpoint(dict1)
def check_allowunknown_true_wrong_account(ctx):
    """
    RHEVM-18381
        Wrong account to login into remote machine
        with "allowUnknow" is true in cockpit
    """
    log.info("Wrong account to login into remote machine with 'allowUnknow' is true in cockpit...")
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_wrong_account(second_ip)


@checkpoint(dict1)
def check_allowunknown_true_remote_closed(ctx):
    """
    RHEVM-18382
        Login remote closed host with "allowUnknow" is true in cockpit
    """
    log.info("Trying to login remote closed host with 'allowUnknow' is true in cockpit...")
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_remote_closed(second_ip, "root", second_password)


@checkpoint(dict1)
def check_allowunknown_true_wrong_address(ctx):
    """
    RHEVM-18383
        Login remote host with wrong address in cockpit
    """
    log.info("Trying to login remote host with wrong address in cockpit...")
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_wrong_address()


@checkpoint(dict1)
def check_allowunknown_true_empty_username(ctx):
    """
    RHEVM-18384
        Login remote host with wrong address in cockpit
    """
    log.info("Trying to login remote host with wrong address in cockpit...")
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true_empty_username(second_ip, "root", second_password)


@checkpoint(dict1)
def check_allowunknown_true(ctx):
    """
    RHEVM-18380
        Login into remote machine with "allowUnknown" is true in cockpit
    """
    log.info("Trying to login into remote machine with 'allowUnknow' is true in cockpit ...")
    login_page = LoginPage(ctx)
    login_page.check_allow_unknown_true(second_ip, "root", second_password)


@checkpoint(dict1)
def check_system_login_host(ctx):
    """
    RHEVM-18377
        Login cockpit via Firefox browser
    """
    log.info("Trying to login cockpit via Firefox browser...")
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_incorrect_credential()
    time.sleep(2)
    login_page.login_with_credential(host_user, host_password)
    system_page = SystemPage(ctx)
    system_page.check_login_host(host_ip)


@checkpoint(dict1)
def check_system_configure_hostname(ctx):
    """
    RHEVM-18385
        Configure hostname
    """
    log.info("Trying to configure hostname...")
    system_page = SystemPage(ctx)
    system_page.configure_hostname()
    system_page.check_configure_hostname()


@checkpoint(dict1)
def check_system_configure_timezone(ctx):
    """
    RHEVM-18386
        Configure timezone
    """
    log.info("Trying to configure timezone...")
    system_page = SystemPage(ctx)
    system_page.configure_timezone()
    system_page.check_configure_timezone()


@checkpoint(dict1)
def check_system_configure_time(ctx):
    """
    RHEVM-18387
        Configure time manually
    """
    log.info("Trying to configure time manually...")
    system_page = SystemPage(ctx)
    system_page.configure_time()
    system_page.check_configure_time()


@checkpoint(dict1)
def check_change_system_performance_profile(ctx):
    """
    RHEVM-18390
        Change performance profile
    """
    log.info("Trying to change performance profile...")
    system_page = SystemPage(ctx)
    system_page.change_performance_profile()
    system_page.check_change_performance_profile()


def runtest():
    ctx = init_browser()
    test_login(ctx)
    check_another_server(ctx)
    check_dashboard_cpu(ctx)
    check_dashboard_memory(ctx)
    check_dashboard_network(ctx)
    check_dashboard_disk_io(ctx)
    """
    check_ui_logs(ctx)
    check_ui_services(ctx)

    check_allowunknown_default
    check_allowunknown_true
    check_allowunknown_true_empty_username
    check_allowunknown_true_remote_closed
    check_allowunknown_true_wrong_account
    check_allowunknown_true_wrong_address
    
    check_change_system_performance_profile
    check_system_configure_hostname
    check_system_configure_time
    check_system_configure_timezone
    check_system_login_host
    """
    ctx.close()
