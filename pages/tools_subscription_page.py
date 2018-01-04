import logging
import re
from utils.page_objects import PageObject, PageElement, MultiPageElement


log = logging.getLogger("sherry")


class SubscriptionPage(PageObject):
    """Subscription-manager for host to register to RHSM/Satellite server"""
    # frame name
    frame_right_name = "cockpit1:localhost/subscriptions"

    subscription_title = PageElement(css="div.subscription-status-ct>h2")
    status_txt = PageElement(css="div.subscription-status-ct>label")

    # register button
    register_sys_btn = PageElement(css="div.subscription-status-ct>button")

    # Elements after click the register button
    register_dialog_title = PageElement(css="h4.modal-title")
    login_input = PageElement(id_="subscription-register-username")
    passwd_input = PageElement(id_="subscription-register-password")
    key_input = PageElement(id_="subscription-register-key")
    org_input = PageElement(id_="subscription-register-org")
    apply_cancel_btns = MultiPageElement(css="div.modal-footer>button")

    url_select_btn = PageElement(
        xpath=".//*[@id='subscription-register-url']/button")
    url_default_item = PageElement(
        xpath=".//*[@id='subscription-register-url']/ul/li[1]/a")
    url_custom_item = PageElement(
        xpath=".//*[@id='subscription-register-url']/ul/li[2]/a")
    url_input = PageElement(id_="subscription-register-url-custom")

    # Elements under "Installed products"
    installed_product_title = PageElement(css="caption.cockpit-caption")
    installed_product_btn = PageElement(tag_name="th")
    details_titles = MultiPageElement(css="td.form-tr-ct-title")
    details_contents = MultiPageElement(css="td.form-tr-ct-title+td>span")

    def __init__(self, *args, **kwargs):
        super(SubscriptionPage, self).__init__(*args, **kwargs)
        self.get("/subscriptions")
        self.wait(10)

    def basic_check_elements_exists(
        self, 
        version,
        product_name="Red Hat Virtualization Host", 
        product_id="328", 
        arch="x86_64"):

        with self.switch_to_frame(self.frame_right_name):
            assert self.subscription_title.text == 'Subscriptions', \
                "subscription title not correct"
            assert self.status_txt.text == "Status: System isn't registered", \
                "Status not correct"
            assert self.register_sys_btn, "register system btn not exist"
            
            assert self.installed_product_title.text == "Installed products", \
                "installed product title not correct"
            assert self.installed_product_btn.text == product_name, \
                "installed product is {}".format(self.installed_product_btn.text)

            self.installed_product_btn.click()
            self.wait()

            product_name_title = list(self.details_titles)[0]
            product_id_title = list(self.details_titles)[1]
            version_title = list(self.details_titles)[2]
            arch_title = list(self.details_titles)[3]
            status_title = list(self.details_titles)[4]
            start_title = list(self.details_titles)[5]
            end_title = list(self.details_titles)[6]

            product_name_content = list(self.details_contents)[0]
            product_id_content = list(self.details_contents)[1]
            version_content = list(self.details_contents)[2]
            arch_content = list(self.details_contents)[3]
            status_content = list(self.details_contents)[4]
            start_content = list(self.details_contents)[5]
            end_content = list(self.details_contents)[6]

            assert product_name_title.text == "Product name", \
                "product name title not correct"
            assert product_name_content.text == product_name, \
                "product name is {}, not {}".format(
                    product_name_content.text, product_name)
            assert product_id_title.text == "Product ID", \
                "product id title not correct"
            assert product_id_content.text == product_id, \
                "product id is {}, not {}".format(self.product_id_content.text, product_id)
            assert version_title.text == "Version", "Version title not correct"
            assert re.search(version_content.text, version), "Product verison not correct"
            assert arch_title.text == "Architecture", "Arch title not correct"
            assert arch_content.text == arch, "Arch is {}, not {}".format(
                arch_content.text, arch)
            assert status_title.text == "Status", "status title not correct"
            assert status_content.text == "Unknown", \
                "status content is {}, not unkonwn".format(
                    start_content.text)
            assert start_title.text == "Starts", "start title not correct"
            assert start_content.text == "", \
                "start content is {}, not none".format(start_content.text)
            assert end_title.text == "Ends", "end title not correct"
            assert end_content.text == "", \
                "end content is {}, not none".format(end_content.text)
