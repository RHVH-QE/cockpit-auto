from selenium import webdriver
from cases import CONF
from pages.common.login_page import LoginPage
import logging

log = logging.getLogger("sherry")



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
        #return None
    else:
        raise NotImplementedError


def test_login(ctx):
    log.info("Start to run test common cases...")
    log.info("Test common_tools-->Login to the browser...")
    try:

        login_page = LoginPage(ctx)
        login_page.basic_check_elements_exists()
        login_page.login_with_credential(host_user, host_password)
        #log.info("['RHEVM:14141']: passed")
        log.info("Common cases tested passed.")
    except Exception as e:
        log.info("Common cases tested failed.")
        log.error(e)
    finally:
        log.info("Finish to run test common cases...")



def runtest():
    ctx = init_browser()
    test_login(ctx)
    ctx.close()
