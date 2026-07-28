# pages/cart_page.py
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        # Initialize the CartPage with the Playwright page object
        super().__init__(page)

    async def verify_cart_is_empty(self):
        # Check if the cart is empty by retrieving the text of the empty cart message
        return await self.get_text('.cart-empty-message')

    async def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        # Locate the total price element in the cart
        total_element = self.page.locator("#totalp")
        # Wait until the total price element is visible
        await total_element.wait_for(state="visible")

        # Retrieve the total price text and convert it to a float
        total_text = await total_element.inner_text()
        actual_total = float(total_text.replace("$", "").replace(",", "").strip())

        # Calculate the maximum allowed budget based on the budget per item and item count
        max_allowed_budget = budget_per_item * items_count

        # Assert that the actual total does not exceed the maximum allowed budget
        assert max_allowed_budget >= actual_total, (
            f"Cart total ({actual_total}) exceeds the allowed budget ({max_allowed_budget}). "
            f"[Budget per item: {budget_per_item}, Items count: {items_count}]"
        )

    async def clean_cart(self):
        delete_button = self.page.locator("a:has-text('Delete')").first

        while await delete_button.is_visible():
            current_item = delete_button

            await current_item.click()

            await current_item.wait_for(state="detached")
