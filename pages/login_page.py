from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        # Initialize the LoginPage with the Playwright page object
        super().__init__(page)
        # Define selectors for the email input, password input, and login button
        self.email_input = '#loginusername'
        self.password_input = '#loginpassword'
        self.login_button = "button:has-text('Log in')"

    async def enter_email(self, email):
        # Enter the provided email into the email input field
        await self.type_text(self.email_input, email)

    async def enter_password(self, password):
        # Enter the provided password into the password input field
        await self.type_text(self.password_input, password)

    async def click_login_button(self):
        # Click the login button to submit the login form
        await self.click_element(self.login_button)

    async def login(self, email, password):
        # Perform the login process by entering email, password, and clicking the login button
        await self.enter_email(email)
        await self.enter_password(password)
        await self.click_login_button()
