# product_page.py
from pathlib import Path
from pages.base_page import BasePage

class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def _add_single_item_to_cart(self, product_name: str):
        async with self.page.expect_event("dialog") as dialog_info:
            async with self.page.expect_response("**/addtocart") as response_info:
                add_to_cart_btn = self.page.locator("a:has-text('Add to cart')")
                await add_to_cart_btn.wait_for(state="visible")
                await add_to_cart_btn.click()

        dialog = await dialog_info.value
        await dialog.accept()

        response = await response_info.value
        assert response.status == 200

        await self.page.locator("a:has-text('Home')").click()

    async def add_product_to_cart(self, product_name: str) -> None:
        await self._add_single_item_to_cart(product_name)

        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        clean_name = product_name.replace(" ", "_")
        screenshot_path = screenshots_dir / f"screenshot_{clean_name}.png"
        await self.page.screenshot(path=str(screenshot_path))