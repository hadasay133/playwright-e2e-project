# pages/cart_page.py
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    async def verify_cart_is_empty(self):
        return await self.get_text('.cart-empty-message')

    async def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        total_element = self.page.locator("#totalp")
        await total_element.wait_for(state="visible")

        total_text = await total_element.inner_text()
        actual_total = float(total_text.replace("$", "").replace(",", "").strip())

        max_allowed_budget = budget_per_item * items_count

        assert max_allowed_budget >= actual_total, (
            f"Cart total ({actual_total}) exceeds the allowed budget ({max_allowed_budget}). "
            f"[Budget per item: {budget_per_item}, Items count: {items_count}]"
        )


    async def clean_cart(self):
        delete_button = self.page.locator("a:has-text('Delete')")
        while await delete_button.is_visible():
            await delete_button.click()
            await self.page.wait_for_timeout(500)  # Optional: Add a small delay to ensure the DOM updates



