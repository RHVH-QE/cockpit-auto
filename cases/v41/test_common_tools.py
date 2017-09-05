from selenium import webdriver
from cases import CONF
from pages.common.login_page import LoginPage
from pages.v41.tools_account_page import AccountPage
from pages.v41.tools_diagnostic_page import DiagnosticPage
from utils.helpers import checkpoint
import logging
import const
import time

log = logging.getLogger("sherry")

dict1 = dict(zip(const.common_tools, const.common_tools_id))

host_ip, host_user, host_password, browser = CONF.get('common').get(
    'host_ip'), CONF.get('common').get('host_user'), CONF.get('common').get(
        'host_password'), CONF.get('common').get('browser')


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
    login_page = LoginPage(ctx)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


@checkpoint(dict1)
def check_create_account(ctx):
    """
    RHEVM-18410
        Create account in cockpit
    """
    accout_page = AccountPage(ctx)
    accout_page.create_new_account()
    accout_page.check_new_account_from_ssh(host_ip)
    accout_page.delete_new_account()


@checkpoint(dict1)
def check_create_diagnostic(ctx):
    """
    RHEVM-18416
        Create diagnostic in cockpit
    """
    diagnostic_page = DiagnosticPage(ctx)
    diagnostic_page.create_sos_report()
    time.sleep(30)
    diagnostic_page.check_sosreport_can_be_downloaded()


def runtest():
    ctx = init_browser()
    test_login(ctx)
    import sys
    from utils.helpers import call_func_by_name
    for ckp in dict1.keys():
        call_func_by_name(sys.modules[__name__], ckp, ctx)
    ctx.close()
