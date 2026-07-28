# pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page

    async def click_element(self, selector):
        await self.page.click(selector)

    async def type_text(self, selector, text):
        await self.page.fill(selector, text)

    async def get_text(self, selector):
        return await self.page.text_content(selector)


