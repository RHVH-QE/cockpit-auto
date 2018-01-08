from utils.page_objects import PageObject, PageElement, MultiPageElement


class AccountPage(PageObject):
    # frame name
    frame_right_name = "cockpit1:localhost/users"

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

    def __init__(self, *args, **kwargs):
        super(AccountPage, self).__init__(*args, **kwargs)
        self.get("/users")
        self.wait(5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.accounts_create_btn, "account create button not exists"
            assert self.cockpit_accounts_div, "cockpit account div not exists"
