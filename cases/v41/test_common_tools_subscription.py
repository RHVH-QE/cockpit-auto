from selenium import webdriver
from pages.common.login_page import LoginPage
from pages.v41.tools_subscriptions_page import SubscriptionsPage
from fabric.api import env, run, settings
from cases import CONF
from collections import OrderedDict
from utils.helpers import checkpoint
import const
import logging
import time

log = logging.getLogger("sherry")

dict1 = OrderedDict(zip(const.common_tools_subscription, const.common_tools_subscription_id))

host_ip, host_user, host_password, browser = CONF.get(
    'common').get('host_ip'), CONF.get('common').get('host_user'), CONF.get(
        'common').get('host_password'), CONF.get('common').get(
            'browser')


ca_path, activation_key, activation_org, rhn_user, \
    rhn_password, satellite_ip, satellite_hostname, \
        satellite_user,satellite_password = CONF.get(
            'subscription').get('ca_path'), CONF.get('subscription').get('activation_key'), CONF.get(
                'subscription').get('activation_org'),CONF.get('subscription').get('rhn_user'),CONF.get(
                    'subscription').get('rhn_password'),CONF.get('subscription').get('satellite_ip'),CONF.get(
                        'subscription').get('satellite_hostname'),CONF.get('subscription').get('satellite_user'),CONF.get(
                            'subscription').get('satellite_password')

ROOT_URI = "https://" + host_ip + ":9090"
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


def test_login(firefox):
    login_page = LoginPage(firefox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


@checkpoint(dict1)
def check_subscription_rhsm(firefox):
    """
    RHEVM-18412
        Subscription to RHSM
    """
    log.info("Subscription to RHSM...")
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.check_register_rhsm(rhn_user, rhn_password)
    time.sleep(5)
    subscriptions_page.check_subscription_result()
    subscriptions_page.unregister_subsciption()


@checkpoint(dict1)
def check_subscription_key(firefox):
    """
    RHEVM-18413
        Subscription to RHSM with key and organization
    """
    log.info("Subscription to RHSM with key and organization")
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.check_register_rhsm_key_org(
        activation_key,
        activation_org)
    time.sleep(5)
    subscriptions_page.check_subscription_result()
    subscriptions_page.unregister_subsciption()


@checkpoint(dict1)
def check_subscription_password(firefox):
    """
    RHEVM-18414
        Check password is encrypted in log after Subscription to RHSM
    """
    log.info("Check password is encrypted in log after subscription to RHSM...")
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.check_register_rhsm(rhn_user, rhn_password)
    subscriptions_page.check_password_encrypted(rhn_password)
    subscriptions_page.unregister_subsciption()


def runtest():
    ctx = init_browser()
    test_login(ctx)
    import sys
    from utils.helpers import call_func_by_name
    for ckp in dict1.keys():
        call_func_by_name(sys.modules[__name__], ckp, ctx)
    ctx.close()
