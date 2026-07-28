# pages/base_page.py
class BasePage:
    def __init__(self, page):
        # Initialize the BasePage with a Playwright page object
        self.page = page

    async def click_element(self, selector):
        # Click on an element specified by the CSS selector
        await self.page.click(selector)

    async def type_text(self, selector, text):
        # Type the given text into an input field specified by the CSS selector
        await self.page.fill(selector, text)

    async def get_text(self, selector):
        # Retrieve and return the text content of an element specified by the CSS selector
        return await self.page.text_content(selector)
