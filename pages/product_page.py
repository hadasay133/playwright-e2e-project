# product_page.py
from pathlib import Path
from pages.base_page import BasePage

class ProductPage(BasePage):
    def __init__(self, page):
        # Initialize the ProductPage with the Playwright page object
        super().__init__(page)

    async def _add_single_item_to_cart(self, product_name: str):
        # Add a single item to the cart and handle the dialog and response events
        async with self.page.expect_event("dialog") as dialog_info:
            async with self.page.expect_response("**/addtocart") as response_info:
                # Locate and click the "Add to cart" button
                add_to_cart_btn = self.page.locator("a:has-text('Add to cart')")
                await add_to_cart_btn.wait_for(state="visible")
                await add_to_cart_btn.click()

        # Accept the dialog that appears after adding the item to the cart
        dialog = await dialog_info.value
        await dialog.accept()

        # Verify that the response status is 200 (success)
        response = await response_info.value
        assert response.status == 200

        # Navigate back to the homepage
        await self.page.locator("a:has-text('Home')").click()

    async def add_product_to_cart(self, product_name: str) -> None:
        # Add a product to the cart and take a screenshot for reporting
        await self._add_single_item_to_cart(product_name)

        # Create the directory for storing screenshots if it doesn't exist
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        # Generate a clean filename for the screenshot
        clean_name = product_name.replace(" ", "_")
        screenshot_path = screenshots_dir / f"screenshot_{clean_name}.png"

        # Take a screenshot of the page and save it to the specified path
        await self.page.screenshot(path=str(screenshot_path))
