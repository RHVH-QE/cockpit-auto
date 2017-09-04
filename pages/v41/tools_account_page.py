import re
from fabric.api import settings, local, run, sudo
from utils.page_objects import PageObject, PageElement, MultiPageElement


class AccountPage(PageObject):
    accounts_create_btn = PageElement(id_="accounts-create")
    cockpit_accounts_div = MultiPageElement(
        class_name="cockpit-account")

    # Elements after click the accounts create page
    real_name_input = PageElement(id_="accounts-create-real-name")
    user_name_input = PageElement(id_="accounts-create-user-name")
    password_input = PageElement(id_="accounts-create-pw1")
    confirm_input = PageElement(id_="accounts-create-pw2")
    access_checkbox = PageElement(id_="accounts-create-locked")
    create_btn = PageElement(id_="accounts-create-create")

    # Elements after click the cockpit-accounts-div
    account_username = PageElement(id_="account-user-name")
    account_delete = PageElement(id_="account-delete")

    # Elements after click the Delete button
    delete_files_checkbox = PageElement(id_="account-confirm-delete-files")
    delete_apply_btn = PageElement(id_="account-confirm-delete-apply")

    # frame name
    frame_right_name = "cockpit1:localhost/users"

    def __init__(self, *args, **kwargs):
        super(AccountPage, self).__init__(*args, **kwargs)
        self.get("/users")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.accounts_create_btn, "account create button not exists"
            assert self.cockpit_account_div, "cockpit account div not exists"

    def create_new_account(self):
        """
        Purpose:
            Create a new account via cockpit
        """
        with self.switch_to_frame(self.frame_right_name):
            self.accounts_create_btn.click()
            self.wait(1)
            self.real_name_input.clear()
            self.wait(1)
            self.real_name_input.send_keys("cockpit")
            self.wait(3)

            self.user_name_input.clear()
            self.wait(1)
            self.user_name_input.send_keys("cockpit")
            self.wait(3)

            self.password_input.clear()
            self.wait(1)
            self.password_input.send_keys("cockpitauto")
            self.wait(3)

            self.confirm_input.clear()
            self.wait(1)
            self.confirm_input.send_keys("cockpitauto")
            self.wait(3)

            self.create_btn.click()

    def check_new_account_from_ssh(self, host_ip):
        """
        Purpose:
            Check the host can be accessed via new account
        """
        cmd = "whoami"
        local_current_user = local(cmd, capture=True)
        print local_current_user
        cmd = "rm -f /home/%s/.ssh/know_hosts" % local_current_user
        local(cmd)
        """
        with settings(
            host_string="cockpit@" + host_ip,
                password="cockpitauto"):
            output = run("whoami")
            assert re.search("cockpit", output), \
                "New account can not be accessed via ssh"
        """
        with settings(warn_only=True):
            output = sudo("whoami", user="cockpit")
            assert re.search("cockpit", output), \
                "New account can not be accessed via ssh"

    def delete_new_account(self):
        """
        Purpose:
            Delete the new created account
        """
        with self.switch_to_frame(self.frame_right_name):
            for each_account in list(self.cockpit_accounts_div):
                each_account.click()
                if re.search("cockpit", self.account_username.text):
                    self.account_delete.click()
                    self.wait(1)
                    self.delete_files_checkbox.click()
                    self.wait(1)
                    self.delete_apply_btn.click()
                    self.wait(1)
                    break
                assert not re.search(
                    "cockpit", self.account_username.text),     \
                    "Failed to delete the account"
