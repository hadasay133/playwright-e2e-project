from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = '#loginusername'
        self.password_input = '#loginpassword'
        self.login_button = "//button[contains(text(), 'Log in')]"

    async def enter_email(self, email):
        await self.type_text(self.email_input, email)

    async def enter_password(self, password):
        await self.type_text(self.password_input, password)

    async def click_login_button(self):
        await self.click_element(self.login_button)

    async def login(self, email, password):
        await self.enter_email(email)
        await self.enter_password(password)
        await self.click_login_button()
